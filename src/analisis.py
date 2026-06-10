# -*- coding: utf-8 -*-
"""Análisis: sensibilidad (tornado), agregación Estado, pensiones, figuras."""
import numpy as np, pandas as pd, copy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import modelo as M

plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
C = {"S0": "#808080", "S1": "#c0392b", "S2": "#2c5f8a", "S3": "#1e8449"}
ESC = {"S0": "Continuidad", "S1": "Sin política", "S2": "Pigouviano", "S3": "Tokenización"}

def run_all():
    tablas = []
    for pf in M.PERFILES:
        t, _ = M.simula_perfil(pf)
        tablas.append(t)
    return pd.concat(tablas, ignore_index=True)

# ---------------------------------------------------------------- base
BASE = run_all()

# ---------------------------------------------------------------- pensiones (memo post-horizonte)
def memo_pension():
    filas = []
    for pf in M.PERFILES:
        rec = M.perdida_pension(pf)
        base_prev = min(pf["bruto"], M.P["base_max_ss"])
        pension = min(0.9 * base_prev, 45_000.0)            # pensión anual aprox sin recorte
        perdida_anual = rec * pension
        # anualidad 18 años de esperanza a los 65, descontada a t=10
        npv = sum(perdida_anual / (1 + M.P["r"]) ** t for t in range(11, 29))
        filas.append(dict(perfil=pf["id"], recorte_pension=rec,
                          perdida_anual=perdida_anual, npv_perdida_pension=npv))
    return pd.DataFrame(filas)

PEN = memo_pension()

# ---------------------------------------------------------------- θ requerido (retención y η=1)
def thetas_requeridos():
    filas = []
    for pf in M.PERFILES:
        w_total = pf["bruto"] + M.ss_empresa(pf["bruto"])
        V = M.P["kappa_V"] * w_total
        FK = (M.P["F_indemn_dias"] / 365) * M.P["antiguedad"] * pf["bruto"] + M.P["K_crist"] * pf["bruto"]
        th_min = max(0, (w_total - FK * M.P["r"]) / V)
        # η0 sin regalía (escenario S1)
        eta0 = BASE.query("perfil==@pf['id'] and escenario=='S1'")["eta"].iloc[0]
        th_eta1 = (1 - eta0) * pf["neto"] / V               # ec. (9) en términos netos
        filas.append(dict(perfil=pf["id"], theta_calibrado=pf["theta"],
                          theta_min_retencion=th_min, theta_eta1=th_eta1, eta0=eta0))
    return pd.DataFrame(filas)

TH = thetas_requeridos()

# ---------------------------------------------------------------- agregación Estado
POBLACION = 165_000          # población objetivo España (Paper 8B §3.3: 150-180k)
PIB = 1_650_000.0            # PIB España ~1,65 billones € (millones)
PRESION = 0.375              # presión fiscal s/ PIB
RENTA_PC = 33_000.0          # PIB per cápita aprox

def agrega_estado():
    filas = []
    for esc in ["S0", "S1", "S2", "S3"]:
        npv_med = BASE.query("escenario==@esc")["npv_estado"].mean()
        coste_vs_s0 = BASE.query("escenario=='S0'")["npv_estado"].mean() - npv_med
        total_M = coste_vs_s0 * POBLACION / 1e6            # millones €, NPV 10 años
        anual_M = total_M * M.P["r"] / (1 - (1 + M.P["r"]) ** -M.P["T"])  # anualidad equivalente
        filas.append(dict(
            escenario=esc, npv_estado_por_trabajador=npv_med,
            coste_fiscal_npv_por_trab=coste_vs_s0,
            coste_total_M=total_M, anualidad_M=anual_M,
            pct_PIB_anual=100 * anual_M / PIB,
            delta_presion_pp=100 * anual_M / PIB,           # p.p. de presión fiscal para cubrirlo
            delta_esfuerzo_frank=100 * (anual_M / PIB) / (RENTA_PC / 1000) * 1000 / RENTA_PC * 100,
        ))
    df = pd.DataFrame(filas)
    # índice de Frank: presión/renta pc; Δesfuerzo relativo = Δpresión/presión
    df["delta_esfuerzo_pct"] = 100 * (df["pct_PIB_anual"] / 100) / PRESION
    return df.drop(columns=["delta_esfuerzo_frank"])

AGG = agrega_estado()

# ---------------------------------------------------------------- sensibilidad (tornado)
SENS_VARS = [
    ("kappa_V", 1.0, 3.0), ("tau", 0.10, 0.30), ("c_tax", 0.05, 0.15),
    ("hazard_reempleo", 0.05, 0.25), ("penal_salarial", 0.15, 0.40),
    ("r", 0.02, 0.05), ("regalia_rcm", False, True),
]
THETA_RANGOS = {"P1": (0.05, 0.12), "P2": (0.01, 0.05), "P3": (0.12, 0.20)}

def metric(df, quien):
    """Diferencial S3−S2 (tokenización vs pigouviano), media de perfiles."""
    col = {"trabajador": "npv_trabajador", "estado": "npv_estado", "firma": "npv_firma"}[quien]
    s3 = df.query("escenario=='S3'")[col].mean()
    s2 = df.query("escenario=='S2'")[col].mean()
    return s3 - s2

def tornado(quien):
    base_val = metric(BASE, quien)
    filas = []
    for var, lo, hi in SENS_VARS:
        vals = []
        for v in (lo, hi):
            old = M.P[var]; M.P[var] = v
            vals.append(metric(run_all(), quien))
            M.P[var] = old
        filas.append(dict(variable=var, bajo=vals[0], alto=vals[1], base=base_val))
    # θ por tramo (varía por perfil)
    olds = {pf["id"]: pf["theta"] for pf in M.PERFILES}
    vals = []
    for idx in (0, 1):
        for pf in M.PERFILES:
            pf["theta"] = THETA_RANGOS[pf["id"]][idx]
        vals.append(metric(run_all(), quien))
    for pf in M.PERFILES:
        pf["theta"] = olds[pf["id"]]
    filas.append(dict(variable="theta (tramo §3.3)", bajo=vals[0], alto=vals[1], base=base_val))
    df = pd.DataFrame(filas)
    df["amplitud"] = (df["alto"] - df["bajo"]).abs()
    return df.sort_values("amplitud")

TOR_W = tornado("trabajador")
TOR_E = tornado("estado")
TOR_F = tornado("firma")

# ---------------------------------------------------------------- figuras
def fig_trayectorias():
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4), sharey=False)
    for ax, pf in zip(axes, M.PERFILES):
        ajuste = M.calibra_ajuste(pf)
        des = M.trayectoria_desempleo(pf, ajuste)
        t = np.arange(1, M.P["T"] + 1)
        tabla, _ = M.simula_perfil(pf)
        w_total = pf["bruto"] + M.ss_empresa(pf["bruto"]); V = M.P["kappa_V"] * w_total
        regalia = pf["theta"] * V
        imp_reg = M.irpf_rcm(regalia)
        recauda = M.P["tau"] * w_total; transfer = recauda * (1 - M.P["c_tax"])
        irpf_tr = M._progresivo(transfer, M.TRAMOS_IRPF) * 0.5
        ax.plot(t, [pf["neto"]] * len(t), color=C["S0"], lw=1.4, label=ESC["S0"])
        ax.plot(t, des["neto"], color=C["S1"], lw=1.4, label=ESC["S1"])
        ax.plot(t, des["neto"] + transfer - irpf_tr, color=C["S2"], lw=1.4, label=ESC["S2"])
        ax.plot(t, des["neto"] + regalia - imp_reg, color=C["S3"], lw=1.4, label=ESC["S3"])
        ax.set_title(f"{pf['id']} — {pf['nombre']}", fontsize=9)
        ax.set_xlabel("Año (edad 55→65)"); ax.set_ylim(0, None)
    axes[0].set_ylabel("Renta neta anual esperada (€)")
    axes[1].legend(frameon=False, fontsize=8, ncol=2, loc="lower right")
    fig.suptitle("Renta disponible del trabajador desplazado: pigouviano vs. tokenización", y=1.02, fontsize=10)
    fig.tight_layout(); fig.savefig("/home/claude/sim/fig1_trayectorias.png", dpi=160, bbox_inches="tight")

def fig_estado():
    fig, ax = plt.subplots(figsize=(7, 3.6))
    d = AGG.query("escenario!='S0'")
    x = np.arange(len(d))
    ax.bar(x, d["anualidad_M"], color=[C[e] for e in d["escenario"]], width=0.6)
    for i, (_, r) in enumerate(d.iterrows()):
        ax.text(i, r["anualidad_M"] + 20, f"{r['anualidad_M']:,.0f} M€/año\n({r['pct_PIB_anual']:.3f}% PIB)",
                ha="center", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels([ESC[e] for e in d["escenario"]])
    ax.set_ylabel("Coste fiscal anual equivalente (M€)")
    ax.set_title(f"Coste para el Estado vs. continuidad — población objetivo {POBLACION:,} trabajadores", fontsize=10)
    fig.tight_layout(); fig.savefig("/home/claude/sim/fig2_estado.png", dpi=160, bbox_inches="tight")

def fig_tornado():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8))
    for ax, (tor, titulo) in zip(axes, [(TOR_W, "Trabajador"), (TOR_F, "Firma"), (TOR_E, "Estado")]):
        y = np.arange(len(tor))
        ax.barh(y, tor["alto"] - tor["base"], left=tor["base"], color="#1e8449", alpha=.75, label="valor alto")
        ax.barh(y, tor["bajo"] - tor["base"], left=tor["base"], color="#c0392b", alpha=.75, label="valor bajo")
        ax.axvline(tor["base"].iloc[0], color="k", lw=0.8)
        ax.set_yticks(y); ax.set_yticklabels(tor["variable"], fontsize=8)
        ax.set_title(f"{titulo}: NPV(S3−S2)", fontsize=9)
        ax.set_xlabel("€ por trabajador (10 años, NPV)")
    axes[0].legend(frameon=False, fontsize=8)
    fig.suptitle("Sensibilidad del diferencial tokenización − pigouviano", y=1.03, fontsize=10)
    fig.tight_layout(); fig.savefig("/home/claude/sim/fig3_tornado.png", dpi=160, bbox_inches="tight")

if __name__ == "__main__":
    fig_trayectorias(); fig_estado(); fig_tornado()
    print("=== THETAS REQUERIDOS ===\n", TH.to_string(index=False))
    print("\n=== PENSIONES (memo) ===\n", PEN.to_string(index=False))
    print("\n=== AGREGADO ESTADO ===\n", AGG.to_string(index=False))
    print("\n=== TORNADO TRABAJADOR ===\n", TOR_W.to_string(index=False))
    print("\n=== TORNADO ESTADO ===\n", TOR_E.to_string(index=False))
    print("\n=== TORNADO FIRMA ===\n", TOR_F.to_string(index=False))
    TH.to_csv("/home/claude/sim/thetas.csv", index=False)
    PEN.to_csv("/home/claude/sim/pensiones.csv", index=False)
    AGG.to_csv("/home/claude/sim/agregado_estado.csv", index=False)
    pd.concat([TOR_W.assign(actor="trabajador"), TOR_E.assign(actor="estado"),
               TOR_F.assign(actor="firma")]).to_csv("/home/claude/sim/tornado.csv", index=False)
