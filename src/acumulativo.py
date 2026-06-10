# -*- coding: utf-8 -*-
"""
S4 — Sistema de royalties ACUMULATIVO (wallet custodiada).
Cada año trabajado genera derechos sobre la cosecha (vintage) de proyectos de ese año.
El flujo de cada vintage decae al 15% anual (vida media geométrica ≈ 6,7 años ≈ 6 años).
Los derechos se abonan como tokens a una wallet personal custodiada por la empresa,
con rendimiento anual r_w ∈ [0,5%, 1,9%] (base 1,2%). Tributación RCM en el devengo.
Carrera: 20 años (edad 35→55). Desplazamiento a los 55. Horizonte de comparación: 55→65.
Consistencia con S3 plano: valor de vintage v = δ_p·V, de modo que el flujo estacionario
de regalía en empleo converge a θ·V (mismo flujo que el sistema plano).
"""
import numpy as np, pandas as pd
import importlib, modelo as M
importlib.reload(M)
M.P["earmark_integro"] = True

DECAY = 0.15          # rendimientos decrecientes del proyecto (15%/año) -> vida media ~6,7 años
RW_BASE, RW_LO, RW_HI = 0.012, 0.005, 0.019
CARRERA = 20          # años de acumulación (edad 35 -> 55)

def sistema_acumulativo(pf, rw=RW_BASE):
    """Devuelve: serie de devengos brutos/netos por edad (36..65), saldo de wallet,
    y renta disponible post-desplazamiento (55->65)."""
    w_total = pf["bruto"] + M.ss_empresa(pf["bruto"])
    V = M.P["kappa_V"] * w_total
    thetaV = pf["theta"] * V

    # Devengo bruto de regalías por año de carrera s=1..20 (suma de vintages vivos):
    # g_s = θ·V·(1 − 0.85^s)  — rampa hacia el flujo estacionario θ·V
    devengo_empleo = np.array([thetaV * (1 - (1 - DECAY) ** s) for s in range(1, CARRERA + 1)])
    # Post-desplazamiento u=1..10: sin vintages nuevos, el stock decae
    g20 = thetaV * (1 - (1 - DECAY) ** CARRERA)
    devengo_post = np.array([g20 * (1 - DECAY) ** u for u in range(1, M.P["T"] + 1)])

    # Wallet durante el empleo: devengo neto de RCM se capitaliza a rw (rendimiento neto de RCM 19%)
    rw_neto = rw * (1 - 0.19)
    W = 0.0; saldo = []
    for g in devengo_empleo:
        g_neto = g - M.irpf_rcm(g)
        W = W * (1 + rw_neto) + g_neto
        saldo.append(W)
    W0 = W  # saldo a los 55

    # Post-desplazamiento: regalías decrecientes cobradas en efectivo (netas de RCM)
    # + anualidad de retirada de W0 a 10 años al tipo rw_neto
    anual_W0 = W0 * rw_neto / (1 - (1 + rw_neto) ** -M.P["T"]) if rw_neto > 0 else W0 / M.P["T"]
    regalia_neta_post = np.array([g - M.irpf_rcm(g) for g in devengo_post])
    rcm_post = devengo_post - regalia_neta_post
    return dict(devengo_empleo=devengo_empleo, devengo_post=devengo_post,
                saldo_wallet=np.array(saldo), W0=W0, anual_W0=anual_W0,
                regalia_neta_post=regalia_neta_post, rcm_post=rcm_post, thetaV=thetaV)

def simula_S4(pf, rw=RW_BASE):
    """NPV trabajador / Estado / firma en la ventana 55->65, comparable con S1/S2/S3."""
    ajuste = M.calibra_ajuste(pf)
    des = M.trayectoria_desempleo(pf, ajuste)
    ac = sistema_acumulativo(pf, rw)
    w_total = pf["bruto"] + M.ss_empresa(pf["bruto"]); V = M.P["kappa_V"] * w_total
    FK = (M.P["F_indemn_dias"] / 365) * M.P["antiguedad"] * pf["bruto"] + M.P["K_crist"] * pf["bruto"]

    neto4, estado4, firma4 = [], [], []
    Wt = ac["W0"]
    for k, row in enumerate(des.itertuples()):
        ingreso = row.neto + ac["regalia_neta_post"][k] + ac["anual_W0"]
        neto4.append(ingreso)
        estado4.append(row.irpf + row.ss_w + row.ss_er - row.gasto_estado
                       + ac["rcm_post"][k] + 0.19 * RW_BASE * max(Wt, 0)
                       + M.P["iva_efectivo"] * M.P["mpc"] * ingreso)
        # firma: opera el agente (1·V), paga regalía decreciente, beneficio de financiación barata (r − rw) sobre saldo
        firma4.append(V - ac["devengo_post"][k] * (1 + M.P["c_token"])
                      + (M.P["r"] - rw) * max(Wt, 0))
        Wt = Wt * (1 + rw * (1 - 0.19)) - ac["anual_W0"]
    firma4[0] -= FK
    eta = np.mean(neto4) / pf["neto"]
    return dict(npv_trabajador=M.descuento(neto4), npv_estado=M.descuento(estado4),
                npv_firma=M.descuento(firma4), eta=eta, W0=ac["W0"],
                renta_pc_equiv=np.mean(neto4) / pf["unidades_consumo"], ac=ac, des=des)

# ---------------------------------------------------------------- comparación
if __name__ == "__main__":
    filas = []
    for pf in M.PERFILES:
        s4 = simula_S4(pf)
        for inef in (0.20, 0.35, 0.45):
            M.P["c_tax"] = inef
            t, _ = M.simula_perfil(pf)
            s2 = t.query("escenario=='S2'").iloc[0]
            s3 = t.query("escenario=='S3'").iloc[0]
            s0 = t.query("escenario=='S0'").iloc[0]
            filas.append(dict(perfil=pf["id"], ineficiencia=inef,
                eta_S2=round(s2.eta, 3), eta_S3plano=round(s3.eta, 3), eta_S4acum=round(s4["eta"], 3),
                trab_S2=round(s2.npv_trabajador), trab_S3=round(s3.npv_trabajador),
                trab_S4=round(s4["npv_trabajador"]),
                dif_S4_S2=round(s4["npv_trabajador"] - s2.npv_trabajador),
                estado_S4=round(s4["npv_estado"]),
                coste_fiscal_S2=round(s0.npv_estado - s2.npv_estado),
                coste_fiscal_S4=round(s0.npv_estado - s4["npv_estado"]),
                firma_S4=round(s4["npv_firma"]),
                bienestar_S4_menos_S2=round((s4["npv_trabajador"] + s4["npv_estado"] + s4["npv_firma"])
                                            - (s2.npv_trabajador + s2.npv_estado + s2.npv_firma)),
                W0_wallet=round(s4["W0"]), pc_equiv_S4=round(s4["renta_pc_equiv"])))
    D = pd.DataFrame(filas)
    pd.set_option("display.width", 260)
    print(D.to_string(index=False))
    D.to_csv("/home/claude/sim/resultados_acumulativo.csv", index=False)

    # sensibilidad de la wallet al rendimiento
    print("\nSensibilidad r_w (saldo W0 y NPV trabajador, base i=35%):")
    for pf in M.PERFILES:
        lo, mid, hi = (simula_S4(pf, r) for r in (RW_LO, RW_BASE, RW_HI))
        print(f"  {pf['id']}: W0 = {lo['W0']:,.0f} / {mid['W0']:,.0f} / {hi['W0']:,.0f} €  ->"
              f" NPV trab = {lo['npv_trabajador']:,.0f} / {mid['npv_trabajador']:,.0f} / {hi['npv_trabajador']:,.0f} €")
