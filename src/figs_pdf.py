# -*- coding: utf-8 -*-
"""Figuras bilingües para el informe PDF (ES/EN)."""
import numpy as np, pandas as pd, importlib, warnings
warnings.filterwarnings("ignore")
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys; sys.path.insert(0, "/home/claude/sim")
import modelo as M, acumulativo as A, fronteras as FR

plt.rcParams.update({"font.size":9,"axes.spines.top":False,"axes.spines.right":False,
                     "figure.facecolor":"white"})
BLUE, GREEN, GRAY, RED = "#2456A6", "#1E7A52", "#8A949C", "#B4232A"

L = {
 "es": dict(age="Edad", income="Renta neta anual (€)", cont="Continuidad", pig="Pigouviano", roy="Royalties (acumulativo)",
   wallet="Saldo wallet (eje dcho., €)", desp="despido (55)", f5t="Evolución temporal de ambos sistemas (perfil P94, España)",
   f6t="θ mínimo para que el royalty domine al impuesto (trabajador, despido a 55)",
   tau="τ pigouviano (%)", thstar="θ* de indiferencia (%)", inef="Ineficiencia fiscal",
   f7t="La edad de desplazamiento invierte el ranking", flat="Arquitectura plana", cum="Arquitectura acumulativa",
   ageD="Edad de desplazamiento", f8t="Estructura impositiva por país: los tres determinantes",
   wedge="Cuña fiscal total", eta0="η₀ sin mecanismo", capt="Fiscalidad del capital (royalty)",
   f9t="Coste para la empresa y zona de contratación", cost="Coste anual por trabajador (€)",
   tax20="Impuesto (τ=20%)", roy10="Royalty devengado (θ=10%)", roynet="Royalty neto de financiación",
   firmline="θ máx. de la firma", workline="θ mín. del trabajador", zone="Zona de contratación",
   theta_pc="θ (%)"),
 "en": dict(age="Age", income="Annual net income (€)", cont="Continuity", pig="Pigouvian", roy="Royalties (cumulative)",
   wallet="Wallet balance (right axis, €)", desp="dismissal (55)", f5t="Time evolution of both systems (P94 profile, Spain)",
   f6t="Minimum θ for royalties to dominate the tax (worker, dismissal at 55)",
   tau="Pigouvian τ (%)", thstar="Indifference θ* (%)", inef="Fiscal inefficiency",
   f7t="Displacement age reverses the ranking", flat="Flat architecture", cum="Cumulative architecture",
   ageD="Displacement age", f8t="Tax structure by country: the three determinants",
   wedge="Total tax wedge", eta0="η₀ with no mechanism", capt="Capital taxation (royalty)",
   f9t="Firm cost and the contracting zone", cost="Annual cost per worker (€)",
   tax20="Tax (τ=20%)", roy10="Royalty accrued (θ=10%)", roynet="Royalty net of financing",
   firmline="Firm max θ", workline="Worker min θ", zone="Contracting zone",
   theta_pc="θ (%)"),
}

G = pd.read_csv("/home/claude/sim/fronteras_theta.csv")
E = pd.read_csv("/home/claude/sim/fronteras_edad.csv")
P = pd.read_csv("/home/claude/sim/estructura_pais.csv")
F = pd.read_csv("/home/claude/sim/frontera_firma.csv")
NAMES = {"es":{"ES":"España","FR":"Francia","DE":"Alemania","IT":"Italia","BE":"Bélgica","PT":"Portugal","UK":"R. Unido","US":"EE. UU.","CA":"Canadá"},
         "en":{"ES":"Spain","FR":"France","DE":"Germany","IT":"Italy","BE":"Belgium","PT":"Portugal","UK":"UK","US":"USA","CA":"Canada"}}

def fig_timeline(lang):
    t = L[lang]; M.P["earmark_integro"]=True; M.P["c_tax"]=0.35
    pf = M.PERFILES[2]  # P3 analista
    ajuste = M.calibra_ajuste(pf); des = M.trayectoria_desempleo(pf, ajuste)
    ac = A.sistema_acumulativo(pf)
    w_total = pf["bruto"]+M.ss_empresa(pf["bruto"]); recauda=.20*w_total; tr=recauda*.65
    irpf_tr = M._progresivo(tr, M.TRAMOS_IRPF)*0.5
    x = np.arange(36,66)
    pig = np.concatenate([np.full(20,pf["neto"]), des["neto"].values+tr-irpf_tr])
    roy = np.concatenate([np.full(20,pf["neto"]), des["neto"].values+ac["regalia_neta_post"]+ac["anual_W0"]])
    rwn=.012*.81; W=ac["W0"]; Wp=[]
    for _ in range(10): W=W*(1+rwn)-ac["anual_W0"]; Wp.append(max(W,0))
    wal = np.concatenate([ac["saldo_wallet"], Wp])
    fig,ax=plt.subplots(figsize=(7.4,3.3))
    ax.plot(x,[pf["neto"]]*30,color=GRAY,ls=":",lw=1.3,label=t["cont"])
    ax.plot(x,pig,color=BLUE,lw=2,label=t["pig"]); ax.plot(x,roy,color=GREEN,lw=2,label=t["roy"])
    ax.axvline(55.5,color=RED,ls="--",lw=.8); ax.text(55.7,pf["neto"]*1.18,t["desp"],fontsize=7.5,color=RED,rotation=90)
    ax2=ax.twinx(); ax2.fill_between(x,0,wal,color=GREEN,alpha=.10); ax2.set_ylim(0,max(wal)*2.4)
    ax2.set_ylabel(t["wallet"],fontsize=8); ax2.spines.right.set_visible(True)
    ax.set_xlabel(t["age"]); ax.set_ylabel(t["income"]); ax.set_ylim(0,pf["neto"]*1.45)
    ax.legend(fontsize=8,frameon=False,loc="lower left"); ax.set_title(t["f5t"],fontsize=10)
    fig.tight_layout(); fig.savefig(f"/home/claude/sim/pdf_f1_{lang}.png",dpi=170,bbox_inches="tight"); plt.close()

def fig_frontier(lang):
    t = L[lang]; cols = plt.cm.tab10(np.linspace(0,1,9))
    fig,axes=plt.subplots(1,3,figsize=(8.4,2.9),sharey=True)
    for ax,inef in zip(axes,(0.20,0.35,0.45)):
        for cc,col in zip(NAMES[lang],cols):
            d=G.query("pais==@cc and inef==@inef")
            ax.plot(d["tau"]*100,d["theta_star_cum"]*100,marker="o",ms=3,color=col,lw=1.2,label=NAMES[lang][cc])
        ax.set_title(f"{t['inef']} {int(inef*100)}%",fontsize=8.5); ax.set_xlabel(t["tau"],fontsize=8)
    axes[0].set_ylabel(t["thstar"],fontsize=8); axes[2].legend(fontsize=5.6,frameon=False,ncol=2)
    fig.suptitle(t["f6t"],y=1.04,fontsize=9.5)
    fig.tight_layout(); fig.savefig(f"/home/claude/sim/pdf_f2_{lang}.png",dpi=170,bbox_inches="tight"); plt.close()

def fig_age(lang):
    t=L[lang]; cols = plt.cm.tab10(np.linspace(0,1,9))
    fig,axes=plt.subplots(1,2,figsize=(7.4,2.9),sharey=True)
    for ax,arch,ttl in zip(axes,("flat","cum"),(t["flat"],t["cum"])):
        for cc,col in zip(NAMES[lang],cols):
            d=E.query("pais==@cc and arch==@arch")
            ax.plot(d["edad"],d["theta_star"]*100,marker="o",ms=3,color=col,lw=1.2,label=NAMES[lang][cc])
        ax.set_title(ttl+" (τ=20%, i=35%)",fontsize=8.5); ax.set_xlabel(t["ageD"],fontsize=8); ax.set_xticks([45,50,55,60])
    axes[0].set_ylabel(t["thstar"],fontsize=8); axes[1].legend(fontsize=5.6,frameon=False,ncol=2)
    fig.suptitle(t["f7t"],y=1.04,fontsize=9.5)
    fig.tight_layout(); fig.savefig(f"/home/claude/sim/pdf_f3_{lang}.png",dpi=170,bbox_inches="tight"); plt.close()

def fig_country(lang):
    t=L[lang]; Ps=P.sort_values("cuna_total",ascending=False).reset_index()
    x=np.arange(len(Ps))
    fig,ax=plt.subplots(figsize=(7.4,3.0))
    ax.bar(x-0.2,Ps["cuna_total"]*100,width=0.4,color=BLUE,label=t["wedge"])
    ax.bar(x+0.2,Ps["eta0"]*100,width=0.4,color=GRAY,label=t["eta0"])
    ax2=ax.twinx(); ax2.plot(x,Ps["capT"]*100,"s--",color=GREEN,ms=5,label=t["capt"]); ax2.spines.right.set_visible(True)
    ax.set_xticks(x); ax.set_xticklabels([NAMES[lang][p] for p in Ps["pais"]],fontsize=7.5)
    ax.set_ylabel("%"); h1,l1=ax.get_legend_handles_labels(); h2,l2=ax2.get_legend_handles_labels()
    ax.legend(h1+h2,l1+l2,fontsize=7.5,frameon=False); ax.set_title(t["f8t"],fontsize=10)
    fig.tight_layout(); fig.savefig(f"/home/claude/sim/pdf_f4_{lang}.png",dpi=170,bbox_inches="tight"); plt.close()

def fig_firm(lang):
    t=L[lang]
    g, erSSC=62000,.31; wI=g*1.31; V=1.8*wI; DEC=.15
    ages=np.arange(36,66); thetaV=.10*V
    rc=[thetaV*(1-(1-DEC)**s) for s in range(1,21)]
    g20=rc[-1]; rc+= [g20*(1-DEC)**u for u in range(1,11)]
    pc=[0]*20+[.20*wI]*10
    W=0; rW=.01; fb=[]
    Ws=[]
    for v in rc[:20]: W=W*(1+rW)+v*.79; fb.append(.02*W); Ws.append(W)
    annW=W*(rW/(1-(1+rW)**-10)); Wt=W
    for u in range(10): Wt=max(0,Wt*(1+rW)-annW); fb.append(.02*Wt)
    fig,axes=plt.subplots(1,2,figsize=(7.6,3.0))
    axes[0].plot(ages,pc,color=BLUE,lw=2,label=t["tax20"])
    axes[0].plot(ages,rc,color=GREEN,lw=2,label=t["roy10"])
    axes[0].plot(ages,np.array(rc)-np.array(fb),color=GREEN,lw=1.3,ls="--",label=t["roynet"])
    axes[0].axvline(55.5,color="k",ls=":",lw=.7)
    axes[0].set_xlabel(t["age"],fontsize=8); axes[0].set_ylabel(t["cost"],fontsize=8); axes[0].legend(fontsize=7,frameon=False)
    taus=np.array([.10,.20,.30,.40])
    firm=F.query("spread==0.02").sort_values("tau")
    work=np.array([.019,.038,.057,.076])  # θ*_w aprox lineal (i=35%, ES)
    axes[1].plot(taus*100,firm["theta_firm"]*100,marker="o",ms=4,color="#7A4A9E",label=t["firmline"])
    axes[1].plot(taus*100,work*100,marker="s",ms=4,color="#C77A2E",label=t["workline"])
    axes[1].fill_between(taus*100,work*100,firm["theta_firm"]*100,where=firm["theta_firm"].values>work,
                         color=GREEN,alpha=.15,label=t["zone"])
    axes[1].set_xlabel(t["tau"],fontsize=8); axes[1].set_ylabel(t["theta_pc"],fontsize=8); axes[1].legend(fontsize=7,frameon=False)
    fig.suptitle(t["f9t"],y=1.02,fontsize=9.5)
    fig.tight_layout(); fig.savefig(f"/home/claude/sim/pdf_f5_{lang}.png",dpi=170,bbox_inches="tight"); plt.close()

for lang in ("es","en"):
    fig_timeline(lang); fig_frontier(lang); fig_age(lang); fig_country(lang); fig_firm(lang)
print("10 figuras generadas")
