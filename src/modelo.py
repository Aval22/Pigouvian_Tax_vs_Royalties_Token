# -*- coding: utf-8 -*-
"""
Simulación Paper 8B v1.7 — Impuesto pigouviano vs. derecho residual tokenizado (θ·V)
Horizonte: 10 años (edad 55 → 65, jubilación). Tres perfiles profesionales españoles.
Escenarios:
  S0  Continuidad           : sin automatización (contrafactual de referencia)
  S1  Automatización libre  : sustitución agéntica sin política correctiva
  S2  Pigouviano            : sustitución + impuesto τ sobre el ahorro laboral, redistribuido (coste admin c_tax)
  S3  Tokenización          : derecho residual θ_j·V_j ; retención si θ ≥ θ_min (ec. 8), si no, desplazamiento con regalía (ec. 9)
Autor del marco: A. García-Lluis Valencia (Paper 8B v1.7, ecs. 5-9; calibración §3.3)
"""
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# 1. PARÁMETROS GLOBALES (caso base; sensibilidad en sensibilidad.py)
# ----------------------------------------------------------------------------
P = dict(
    T=10,                  # horizonte (años), edad 55 -> 65
    r=0.03,                # tasa de descuento real
    kappa_V=1.5,           # multiplicador V_j = kappa_V * coste laboral total (valor del activo agéntico)
    tau=0.20,              # tipo pigouviano sobre el ahorro de coste laboral (τ* = f(1-1/N), N=10 -> 0.9f)
    c_tax=0.10,            # coste administrativo del canal fiscal (Card-Kluve-Weber: 5-15%)
    c_token=0.01,          # coste de plataforma de tokenización (s/ flujo θV)
    er_ss=0.31,            # cotización empresarial (sobre base topada)
    base_max_ss=60_000.0,  # base máxima de cotización anual (~4.970 €/mes, 2026)
    ipc_plus=0.0,          # términos reales
    hazard_reempleo=0.15,  # probabilidad anual de recolocación (>55 años, España)
    penal_salarial=0.28,   # pérdida salarial media en la recolocación (seniors)
    iprem_mes=600.0,
    mpc=0.85,              # propensión marginal a consumir (trabajadores)
    iva_efectivo=0.10,     # tipo efectivo de imposición al consumo
    F_indemn_dias=33,      # despido improcedente/objetivo mejorado: 33 días/año
    antiguedad=20,         # años de antigüedad al despido
    K_crist=0.50,          # coste de cristalización K_j (fracción del bruto anual)
    regalia_rcm=True,      # θV tributa como rendimiento de capital mobiliario (vs. trabajo)
    pension_anios_br=25,   # años de cómputo de base reguladora
    earmark_integro=False, # True: recaudación pigouviana íntegramente afectada a compensación;
                           #       c_tax pasa a ser pérdida de ineficiencia (peso muerto), el Estado no retiene nada
)

# ----------------------------------------------------------------------------
# 2. PERFILES (datos calculadora Cinco Días aportados por el usuario)
# ----------------------------------------------------------------------------
# OAXI norm = percentil-rank normalizado; θ según tabla §3.3 Paper 8B
PERFILES = [
    dict(id="P1", nombre="Ingeniero/a senior (60k)", bruto=60_000.0, irpf=13_464.00,
         ss_w=3_819.60, neto=42_716.40, oaxi_norm=0.92, theta=0.08,
         hijos=2, unidades_consumo=2.1, tope_paro_mes=1_575.0,
         ocupacion="Ingenieros y Licenciados — tramo P90–P95 OAXI"),
    dict(id="P2", nombre="Técnico/a (52k)", bruto=52_000.0, irpf=10_675.60,
         ss_w=3_369.60, neto=37_954.80, oaxi_norm=0.70, theta=0.03,
         hijos=0, unidades_consumo=1.5, tope_paro_mes=1_225.0,
         ocupacion="Ing. Técnicos/Peritos — tramo P50–P90 OAXI"),
    dict(id="P3", nombre="Analista BI/Crédito (77,5k)", bruto=77_500.0, irpf=18_553.50,
         ss_w=3_854.80, neto=55_091.70, oaxi_norm=0.95, theta=0.15,
         hijos=2, unidades_consumo=2.1, tope_paro_mes=1_575.0,
         ocupacion="Analistas de inteligencia de negocio/riesgo — Top 20 OAXI"),
]

# ----------------------------------------------------------------------------
# 3. FISCALIDAD
# ----------------------------------------------------------------------------
TRAMOS_IRPF = [(12_450, .19), (20_200, .24), (35_200, .30), (60_000, .37), (300_000, .45), (np.inf, .47)]
TRAMOS_RCM  = [(6_000, .19), (50_000, .21), (200_000, .23), (300_000, .27), (np.inf, .28)]

def _progresivo(base, tramos):
    cuota, prev = 0.0, 0.0
    for lim, t in tramos:
        if base > prev:
            cuota += (min(base, lim) - prev) * t
            prev = lim
        else:
            break
    return cuota

def irpf_trabajo(bruto, ss, ajuste=0.0):
    """IRPF aproximado sobre rendimientos del trabajo. 'ajuste' calibra a los datos Cinco Días."""
    base = max(0.0, bruto - ss - 2_000.0)
    cuota = _progresivo(base, TRAMOS_IRPF) - _progresivo(5_550.0, TRAMOS_IRPF) - ajuste
    return max(0.0, cuota)

def calibra_ajuste(perfil):
    """Calibra la deducción residual para que IRPF(bruto)=dato observado (familia, mínimos)."""
    bruto, ss, objetivo = perfil["bruto"], perfil["ss_w"], perfil["irpf"]
    crudo = irpf_trabajo(bruto, ss, 0.0)
    return crudo - objetivo  # deducción fija perfil-específica

def irpf_rcm(base):
    return _progresivo(max(0.0, base), TRAMOS_RCM)

def ss_trabajador(bruto):
    return 0.0647 * min(bruto, P["base_max_ss"])

def ss_empresa(bruto):
    return P["er_ss"] * min(bruto, P["base_max_ss"])

# ----------------------------------------------------------------------------
# 4. CICLO DE DESEMPLEO ESPAÑOL (desplazamiento a los 55 años)
# ----------------------------------------------------------------------------
def trayectoria_desempleo(pf, ajuste):
    """
    Devuelve, por año t=1..T, el ingreso neto ESPERADO del trabajador desplazado sin
    compensación, ponderando la probabilidad de recolocación (hazard anual).
      - Años 1-2: prestación contributiva topada (70%/60% BR, tope por hijos), 24 meses.
      - Año 3+ : subsidio mayores de 52 años (80% IPREM) hasta recolocación o 65.
      - Recolocación: salario = bruto*(1-penalización); búsqueda desde el año 1.
    También devuelve los flujos fiscales asociados (IRPF, SS, prestaciones pagadas).
    """
    T, h = P["T"], P["hazard_reempleo"]
    bruto_re = pf["bruto"] * (1 - P["penal_salarial"])
    ss_re = ss_trabajador(bruto_re)
    irpf_re = irpf_trabajo(bruto_re, ss_re, ajuste)
    neto_re = bruto_re - ss_re - irpf_re

    paro_a1 = pf["tope_paro_mes"] * 6 + pf["tope_paro_mes"] * 6      # tope vinculante en 70% y 60%
    paro_a2 = pf["tope_paro_mes"] * 12
    subsidio = P["iprem_mes"] * 0.80 * 12

    filas = []
    for t in range(1, T + 1):
        s_emp = 1 - (1 - h) ** t            # prob. de estar recolocado en t
        if t == 1:
            bruto_par, tipo = paro_a1, "prestacion"
        elif t == 2:
            bruto_par, tipo = paro_a2, "prestacion"
        else:
            bruto_par, tipo = subsidio, "subsidio"
        irpf_par = irpf_trabajo(bruto_par, 0.0, ajuste) if tipo == "prestacion" else 0.0
        neto_par = bruto_par - irpf_par

        neto_esp = s_emp * neto_re + (1 - s_emp) * neto_par
        filas.append(dict(
            t=t, s_emp=s_emp, neto=neto_esp,
            irpf=s_emp * irpf_re + (1 - s_emp) * irpf_par,
            ss_w=s_emp * ss_re, ss_er=s_emp * ss_empresa(bruto_re),
            gasto_estado=(1 - s_emp) * bruto_par,
        ))
    return pd.DataFrame(filas)

def perdida_pension(pf):
    """Erosión de la base reguladora por desplazamiento a los 55 (memo post-horizonte).
    BR(25a): 15a a base previa topada + 2a prestación (SEPE cotiza por BR) + 8a a 125% base mínima."""
    base_prev = min(pf["bruto"], P["base_max_ss"]) / 12
    base_sub = 1_400.0 * 1.25
    br_sin = base_prev
    br_con = (15 * base_prev + 2 * base_prev + 8 * base_sub) / 25
    return 1 - br_con / br_sin   # % de recorte aproximado de pensión

# ----------------------------------------------------------------------------
# 5. ESCENARIOS
# ----------------------------------------------------------------------------
def descuento(flujos, r=None):
    r = P["r"] if r is None else r
    return sum(f / (1 + r) ** t for t, f in enumerate(flujos, start=1))

def simula_perfil(pf):
    ajuste = calibra_ajuste(pf)
    T = P["T"]
    w_total = pf["bruto"] + ss_empresa(pf["bruto"])          # coste laboral total wᴵ
    V = P["kappa_V"] * w_total                                # flujo del activo agéntico V_j
    FK = (P["F_indemn_dias"] / 365) * P["antiguedad"] * pf["bruto"] + P["K_crist"] * pf["bruto"]
    theta_min = max(0.0, (w_total - FK * P["r"]) / V)         # ec. (8)
    retenido = pf["theta"] >= theta_min

    des = trayectoria_desempleo(pf, ajuste)
    res = {}

    # ---- S0 Continuidad ------------------------------------------------------
    neto0 = [pf["neto"]] * T
    estado0 = [pf["irpf"] + pf["ss_w"] + ss_empresa(pf["bruto"])
               + P["iva_efectivo"] * P["mpc"] * pf["neto"]] * T
    firma0 = [V - w_total] * T   # la firma obtiene V con el trabajador (mismo conocimiento)
    res["S0"] = dict(neto=neto0, estado=estado0, firma=firma0, eta=1.0, retenido=True)

    # ---- S1 Automatización sin política --------------------------------------
    neto1 = list(des["neto"])
    estado1 = [row.irpf + row.ss_w + row.ss_er - row.gasto_estado
               + P["iva_efectivo"] * P["mpc"] * row.neto for row in des.itertuples()]
    firma1 = [V - 0.0 for _ in range(T)]
    firma1[0] -= FK
    res["S1"] = dict(neto=neto1, estado=estado1, firma=firma1,
                     eta=np.mean(neto1) / pf["neto"], retenido=False)

    # ---- S2 Pigouviano --------------------------------------------------------
    recauda = P["tau"] * w_total                              # impuesto anual sobre ahorro laboral
    transfer = recauda * (1 - P["c_tax"])                     # anualidad redistribuida al desplazado
    # la transferencia tributa como rendimiento del trabajo (programa público)
    neto2, estado2 = [], []
    for row in des.itertuples():
        irpf_tr = irpf_trabajo(transfer + (row.neto if False else 0), 0, 0)  # aprox: marginal sobre transfer
        irpf_tr = _progresivo(transfer, TRAMOS_IRPF) * 0.5    # tipo medio reducido aprox sobre transferencia
        neto2.append(row.neto + transfer - irpf_tr)
        if P["earmark_integro"]:
            saldo_programa = 0.0   # recauda − transfer − coste_ineficiencia = 0 (afectación íntegra)
        else:
            saldo_programa = recauda - transfer
        estado2.append(row.irpf + row.ss_w + row.ss_er - row.gasto_estado
                       + saldo_programa + irpf_tr
                       + P["iva_efectivo"] * P["mpc"] * (row.neto + transfer - irpf_tr))
    firma2 = [V - recauda for _ in range(T)]
    firma2[0] -= FK
    res["S2"] = dict(neto=neto2, estado=estado2, firma=firma2,
                     eta=np.mean(neto2) / pf["neto"], retenido=False)

    # ---- S3 Tokenización ------------------------------------------------------
    regalia = pf["theta"] * V
    imp_reg = irpf_rcm(regalia) if P["regalia_rcm"] else _progresivo(regalia, TRAMOS_IRPF)
    if retenido:
        neto3 = [pf["neto"] + regalia - imp_reg] * T
        estado3 = [pf["irpf"] + pf["ss_w"] + ss_empresa(pf["bruto"]) + imp_reg
                   + P["iva_efectivo"] * P["mpc"] * (pf["neto"] + regalia - imp_reg)] * T
        firma3 = [V - w_total - regalia * (1 + P["c_token"])] * T
    else:
        neto3 = [row.neto + regalia - imp_reg for row in des.itertuples()]
        estado3 = [row.irpf + row.ss_w + row.ss_er - row.gasto_estado + imp_reg
                   + P["iva_efectivo"] * P["mpc"] * (row.neto + regalia - imp_reg)
                   for row in des.itertuples()]
        firma3 = [(1 - pf["theta"]) * V - regalia * P["c_token"] for _ in range(T)]
        firma3[0] -= FK
    res["S3"] = dict(neto=neto3, estado=estado3, firma=firma3,
                     eta=np.mean(neto3) / pf["neto"], retenido=retenido)

    # ---- métricas ------------------------------------------------------------
    out = []
    for esc, d in res.items():
        out.append(dict(
            perfil=pf["id"], escenario=esc,
            npv_trabajador=descuento(d["neto"]),
            npv_estado=descuento(d["estado"]),
            npv_firma=descuento(d["firma"]),
            eta=d["eta"], retenido=d["retenido"],
            renta_pc_equiv=np.mean(d["neto"]) / pf["unidades_consumo"],
            theta_min=theta_min, regalia_anual=regalia if esc == "S3" else np.nan,
            perdida_pension=perdida_pension(pf) if esc in ("S1", "S2") or (esc == "S3" and not d["retenido"]) else 0.0,
        ))
    return pd.DataFrame(out), des

# ----------------------------------------------------------------------------
if __name__ == "__main__":
    tablas = []
    for pf in PERFILES:
        t, _ = simula_perfil(pf)
        tablas.append(t)
    R = pd.concat(tablas, ignore_index=True)
    pd.set_option("display.width", 200, "display.float_format", lambda x: f"{x:,.0f}" if abs(x) > 10 else f"{x:,.3f}")
    print(R.to_string(index=False))
    R.to_csv("/home/claude/sim/resultados_base.csv", index=False)
