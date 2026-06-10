# -*- coding: utf-8 -*-
"""Fronteras de optimalidad: pigouviano vs royalties ITEA. 9 países, edades, arquitecturas."""
import numpy as np, pandas as pd
from scipy.optimize import brentq
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size":8.5,"axes.spines.top":False,"axes.spines.right":False})

C = {  # fiscalidad aprox 2026, moneda local; unCapY=prestación anual topada; assist=asistencial
 "ES":dict(n="España",erSSC=.31,eeR=.0647,eeCap=60000,capT=.21,consT=.10,allow=5550,
   br=[(12450,.19),(20200,.24),(35200,.30),(60000,.37),(300000,.45),(9e9,.47)],unCap=18900,assist=5760,wIdx=1.00,taxM=22),
 "FR":dict(n="Francia",erSSC=.42,eeR=.115,eeCap=9e9,capT=.30,consT=.11,allow=0,
   br=[(11294,0),(28797,.11),(82341,.30),(177106,.41),(9e9,.45)],unCap=21000,assist=6300,wIdx=1.15,taxM=26),
 "DE":dict(n="Alemania",erSSC=.207,eeR=.205,eeCap=90600,capT=.26,consT=.10,allow=0,
   br=[(11604,0),(17005,.20),(66760,.32),(277825,.42),(9e9,.45)],unCap=24000,assist=6700,wIdx=1.30,taxM=33),
 "IT":dict(n="Italia",erSSC=.30,eeR=.0919,eeCap=122295,capT=.26,consT=.11,allow=1880,
   br=[(28000,.23),(50000,.35),(9e9,.43)],unCap=17000,assist=6000,wIdx=0.95,taxM=25),
 "BE":dict(n="Bélgica",erSSC=.27,eeR=.1307,eeCap=9e9,capT=.30,consT=.11,allow=10570,
   br=[(15820,.25),(27920,.40),(48320,.45),(9e9,.50)],unCap=23000,assist=7800,wIdx=1.25,taxM=5),
 "PT":dict(n="Portugal",erSSC=.2375,eeR=.11,eeCap=9e9,capT=.28,consT=.11,allow=4104,
   br=[(7703,.1325),(11623,.18),(16472,.23),(21321,.26),(27146,.3275),(39791,.37),(51997,.435),(81199,.45),(9e9,.48)],
   unCap=15400,assist=6200,wIdx=0.65,taxM=5.5),
 "UK":dict(n="R. Unido",erSSC=.15,eeR=.08,eeCap=50270,capT=.20,consT=.10,allow=0,
   br=[(12570,0),(50270,.20),(125140,.40),(9e9,.45)],unCap=5800,assist=4700,wIdx=1.05,taxM=34),
 "US":dict(n="EE. UU.",erSSC=.095,eeR=.0765,eeCap=176100,capT=.18,consT=.07,allow=14600,
   br=[(11600,.10),(47150,.12),(100525,.22),(191950,.24),(243725,.32),(9e9,.37)],unCap=26000,assist=0,wIdx=1.55,taxM=130),
 "CA":dict(n="Canadá",erSSC=.077,eeR=.0695,eeCap=68500,capT=.22,consT=.09,allow=15705,
   br=[(55867,.225),(111733,.305),(173205,.36),(9e9,.43)],unCap=33500,assist=9000,wIdx=1.30,taxM=21),
}
HAZ, PEN, R, DECAY, SAL0 = 0.15, 0.28, 0.03, 0.15, 62000  # analista P94; bruto base ES

def itax(g, c):
    b = max(0, g - c["allow"]); tax, prev = 0, 0
    for lim, rt in c["br"]:
        if b > prev: tax += (min(b, lim) - prev) * rt; prev = lim
        else: break
    return tax
def net(g, c):
    ssc = c["eeR"] * min(g, c["eeCap"]); it = itax(g - ssc, c)
    return g - ssc - it, ssc, it
def npv(a, r=R): return sum(v/(1+r)**(i+1) for i, v in enumerate(a))

def un_path(g, c, post):
    nb, _, _ = net(g, c); reG = g * (1 - PEN); reN, reS, reI = net(reG, c)
    out = []
    for t in range(1, post + 1):
        s = 1 - (1 - HAZ)**t
        ben = min(.65 * g, c["unCap"]) if t <= 2 else c["assist"]
        bN = ben - (itax(ben, c) if t <= 2 else 0)
        out.append(dict(net=s*reN + (1-s)*bN, tax=s*(reI + reS + c["erSSC"]*reG) + (1-s)*(itax(ben,c) if t<=2 else 0),
                        paid=(1-s)*ben))
    return out, nb

def sim(cc, ageD, arch, theta, tau, inef, kappa=1.8):
    c = C[cc]; g = SAL0 * c["wIdx"]
    career, post = ageD - 35, 65 - ageD
    wI = g + c["erSSC"] * min(g, c["eeCap"]); V = kappa * wI
    un, nb = un_path(g, c, post)
    thetaV = theta * V; rW = 0.5*0 + 0.5*0.02  # wallet 50/50, spread 2%
    transfer = tau * wI * (1 - inef); trN = transfer * (1 - 0.15)
    # carrera
    W, w2, w3, s2, s3 = 0, [], [], [], []
    stC = lambda: net(g,c)[2] + net(g,c)[1] + c["erSSC"]*min(g,c["eeCap"]) + c["consT"]*.85*nb
    for s in range(1, career + 1):
        acc = thetaV*(1-(1-DECAY)**s) if arch=="cum" else 0
        W = W*(1+rW) + acc*(1-c["capT"])
        w2.append(nb); w3.append(nb); s2.append(stC()); s3.append(stC() + acc*c["capT"])
    annW = W*(rW/(1-(1+rW)**-post)) if (W>0 and rW>0) else (W/post if W>0 else 0)
    g0 = thetaV*(1-(1-DECAY)**career) if arch=="cum" else thetaV
    for t in range(1, post + 1):
        u = un[t-1]
        i2 = u["net"] + (trN if t <= min(10, post) else 0)
        gp = g0*(1-DECAY)**t if arch=="cum" else thetaV
        i3 = u["net"] + gp*(1-c["capT"]) + annW
        w2.append(i2); w3.append(i3)
        s2.append(u["tax"] - u["paid"] + (transfer*0.15 if t<=min(10,post) else 0) + c["consT"]*.85*i2)
        s3.append(u["tax"] - u["paid"] + gp*c["capT"] + c["consT"]*.85*i3)
    eta0 = sum(u["net"] for u in un)/post/nb
    eta2 = sum(w2[career:])/post/nb; eta3 = sum(w3[career:])/post/nb
    sC = npv([stC()]*(career+post))
    return dict(w2=npv(w2), w3=npv(w3), eta0=eta0, eta2=eta2, eta3=eta3,
                cost2=sC-npv(s2), cost3=sC-npv(s3), W0=W, wI=wI, V=V, nb=nb)

def theta_star(cc, ageD, arch, tau, inef):
    f = lambda th: sim(cc, ageD, arch, th, tau, inef)["w3"] - sim(cc, ageD, arch, 0, tau, inef)["w2"]
    # ojo: w2 no depende de θ → evalúa una vez
    base2 = sim(cc, ageD, arch, 0, tau, inef)["w2"]
    g = lambda th: sim(cc, ageD, arch, th, tau, inef)["w3"] - base2
    try: return brentq(g, 0.0, 0.6, xtol=1e-4)
    except ValueError: return np.nan

# ---------------- rejillas ----------------
rows = []
for cc in C:
    for tau in (0.10, 0.20, 0.30):
        for inef in (0.20, 0.35, 0.45):
            th = theta_star(cc, 55, "cum", tau, inef)
            thf = theta_star(cc, 55, "flat", tau, inef)
            s = sim(cc, 55, "cum", min(th if not np.isnan(th) else .2,.2), tau, inef)
            rows.append(dict(pais=cc, tau=tau, inef=inef, theta_star_cum=th, theta_star_flat=thf,
                             eta0=s["eta0"]))
G = pd.DataFrame(rows); G.to_csv("/home/claude/sim/fronteras_theta.csv", index=False)

rows = []
for cc in C:
    for ageD in (45, 50, 55, 60):
        for arch in ("flat", "cum"):
            th = theta_star(cc, ageD, arch, 0.20, 0.35)
            s0 = sim(cc, ageD, arch, 0.10, 0.20, 0.35)
            rows.append(dict(pais=cc, edad=ageD, arch=arch, theta_star=th, eta0=s0["eta0"]))
E = pd.DataFrame(rows); E.to_csv("/home/claude/sim/fronteras_edad.csv", index=False)

# estructura país: cuña, eta0, fiscalidad
rows = []
for cc, c in C.items():
    g = SAL0 * c["wIdx"]; nb, ssc, it = net(g, c)
    wI = g + c["erSSC"] * min(g, c["eeCap"])
    rows.append(dict(pais=cc, nombre=c["n"], bruto=g, neto=nb, cuna_total=1-nb/wI,
                     capT=c["capT"], eta0=un_path(g, c, 10)[0] and sum(u["net"] for u in un_path(g,c,10)[0])/10/nb,
                     base_pigou=wI, costeF2=sim(cc,55,"cum",.10,.20,.35)["cost2"],
                     costeF3=sim(cc,55,"cum",.10,.20,.35)["cost3"]))
P = pd.DataFrame(rows); P.to_csv("/home/claude/sim/estructura_pais.csv", index=False)

# ---------------- figuras ----------------
cols = plt.cm.tab10(np.linspace(0,1,9))
fig, axes = plt.subplots(1, 3, figsize=(12, 3.6), sharey=True)
for ax, inef in zip(axes, (0.20, 0.35, 0.45)):
    for (cc, col) in zip(C, cols):
        d = G.query("pais==@cc and inef==@inef")
        ax.plot(d["tau"]*100, d["theta_star_cum"]*100, marker="o", ms=3, color=col, label=C[cc]["n"])
    ax.axhspan(5, 20, alpha=0.06, color="green"); ax.axhspan(0.25, 15, alpha=0.04, color="green")
    ax.set_title(f"Ineficiencia fiscal = {int(inef*100)}%"); ax.set_xlabel("τ pigouviano (%)")
axes[0].set_ylabel("θ* de indiferencia del trabajador (%)\n(acumulativo, despido a 55)")
axes[2].legend(fontsize=6.5, frameon=False, ncol=2)
fig.suptitle("Frontera de optimalidad: θ mínimo para que el royalty domine al impuesto, por país", y=1.03, fontsize=10)
fig.tight_layout(); fig.savefig("/home/claude/sim/fig6_frontera_pais.png", dpi=160, bbox_inches="tight")

fig, axes = plt.subplots(1, 2, figsize=(10, 3.6), sharey=True)
for ax, arch, ttl in zip(axes, ("flat","cum"), ("Arquitectura plana","Arquitectura acumulativa")):
    for (cc, col) in zip(C, cols):
        d = E.query("pais==@cc and arch==@arch")
        ax.plot(d["edad"], d["theta_star"]*100, marker="o", ms=3, color=col, label=C[cc]["n"])
    ax.set_title(ttl + " (τ=20%, i=35%)"); ax.set_xlabel("Edad de desplazamiento"); ax.set_xticks([45,50,55,60])
axes[0].set_ylabel("θ* de indiferencia (%)"); axes[1].legend(fontsize=6.5, frameon=False, ncol=2)
fig.suptitle("Efecto de la edad de desplazamiento sobre la frontera de optimalidad", y=1.03, fontsize=10)
fig.tight_layout(); fig.savefig("/home/claude/sim/fig7_frontera_edad.png", dpi=160, bbox_inches="tight")

fig, ax = plt.subplots(figsize=(9, 3.4))
Ps = P.sort_values("cuna_total", ascending=False)
x = np.arange(len(Ps))
ax.bar(x-0.2, Ps["cuna_total"]*100, width=0.4, color="#2456A6", label="Cuña fiscal total (1−neto/wᴵ)")
ax.bar(x+0.2, Ps["eta0"]*100, width=0.4, color="#8A949C", label="η₀: recuperación sin mecanismo")
ax2 = ax.twinx(); ax2.plot(x, Ps["capT"]*100, "s--", color="#1E7A52", ms=5, label="Fiscalidad del capital (royalty)")
ax.set_xticks(x); ax.set_xticklabels(Ps["nombre"], fontsize=8)
ax.set_ylabel("%"); ax2.set_ylabel("% capital"); ax2.spines.right.set_visible(True)
h1,l1=ax.get_legend_handles_labels(); h2,l2=ax2.get_legend_handles_labels()
ax.legend(h1+h2, l1+l2, fontsize=7.5, frameon=False, loc="upper right")
ax.set_title("Estructura impositiva por país: los tres determinantes de la frontera", fontsize=10)
fig.tight_layout(); fig.savefig("/home/claude/sim/fig8_estructura_pais.png", dpi=160, bbox_inches="tight")

print(G.pivot_table(index="pais", columns=["tau","inef"], values="theta_star_cum").round(3).to_string())
print("\nEDAD:\n", E.pivot_table(index="pais", columns=["arch","edad"], values="theta_star").round(3).to_string())
print("\nPAIS:\n", P.round(3).to_string(index=False))
