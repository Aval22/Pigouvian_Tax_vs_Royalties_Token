# -*- coding: utf-8 -*-
"""Informe PDF didáctico ES/EN: pigouviano vs royalties ITEA."""
from weasyprint import HTML
import base64, os

def img64(p):
    with open(p, "rb") as f: return "data:image/png;base64," + base64.b64encode(f.read()).decode()

C = {
"es": dict(
 lang="es", title="Impuesto pigouviano o royalties por capital intelectual",
 subtitle="¿Qué sistema protege mejor frente al desplazamiento por IA agéntica? Informe didáctico de simulación",
 meta="Marco ITEA · Paper 8B (A. García-Lluis Valencia) · Calibración Forbes Global 2000 · Junio 2026",
 s1h="1 · Qué se compara",
 boxA_t="Sistema A — Impuesto pigouviano", boxA=("La empresa que sustituye a un trabajador por un agente de IA paga un impuesto "
  "(un porcentaje τ del coste laboral que se ahorra). El Estado recauda ese dinero y lo redistribuye al trabajador desplazado como "
  "una transferencia anual. Es un mecanismo <b>ex post</b> (nace cuando ya hubo despido) y <b>fiscal</b> (pasa por la Administración, "
  "que pierde por el camino entre un 20% y un 45% en gestión y distorsiones)."),
 boxB_t="Sistema B — Royalties por transferencia de CI", boxB=("El trabajador cobra cada año un porcentaje θ del valor del activo "
  "algorítmico que su conocimiento ayudó a crear: es el pago por la <i>transferencia de su capital intelectual</i>. Los derechos se "
  "acumulan a lo largo de la carrera (cada proyecto genera una «cosecha» que pierde un 15% de valor al año) y se depositan como tokens "
  "en una <b>wallet</b> custodiada, que puede rentar el IPC, financiar proyectos de la empresa a IPC+spread, o retirarse. Es un mecanismo "
  "<b>ex ante</b> (se devenga mientras se trabaja) y <b>contractual</b> (apenas un 1% de coste de gestión)."),
 keyt="Cinco variables para leer el informe",
 keys=[("θ (theta)","El porcentaje del flujo del activo algorítmico que se paga al trabajador. Es la variable que se negocia. Tramos ITEA: 0,25–15% (percentiles 50–95) y 5–20% (Top 20)."),
  ("τ (tau)","El tipo del impuesto pigouviano sobre el coste laboral ahorrado. La literatura lo sitúa entre el 10% y el 30%."),
  ("η (eta)","La tasa de recuperación de renta: qué fracción de su sueldo neto conserva el trabajador tras el despido. η = 1 significa recuperación plena; sin ningún mecanismo, η ≈ 0,5."),
  ("κ (kappa)","Cuántas veces el coste laboral vale el activo algorítmico (V = κ·wᴵ). Calibrado con el beneficio por empleado de las 2.000 mayores empresas del mundo: entre 1,3 (comercio) y 2,2 (banca)."),
  ("θ* (frontera)","El θ de indiferencia: por debajo, el trabajador prefiere el impuesto; por encima, el royalty. Todo el informe gira en torno a dónde está esta frontera.")],
 s2h="2 · La película completa: de los 35 a los 65 años",
 s2p=("La figura muestra a un analista financiero español (percentil 94 ITEA, 77.500 € brutos) que es desplazado a los 55 años. "
  "La línea gris es su vida sin automatización. La azul es el sistema pigouviano: nada cambia hasta el despido, y después la transferencia "
  "fiscal repone parte de la renta. La verde es el sistema de royalties acumulativo: durante 20 años los derechos de CI se acumulan en la "
  "wallet (área sombreada), que llega al despido con unos 270.000 € — un autoseguro prefinanciado que, sumado a las regalías decrecientes, "
  "sostiene la renta mejor que la transferencia. La clave no es que el royalty pague más: es que paga <b>cuando ocurre la transferencia de "
  "conocimiento</b>, no cuando ocurre el despido."),
 s3h="3 · La frontera θ*: cuánto royalty hace falta para ganar al impuesto",
 s3p=("Para cada país y cada configuración del impuesto calculamos el θ* a partir del cual el trabajador está mejor con royalties. "
  "El resultado es una frontera estrecha y baja: entre el 1,5% y el 7,7% en todo el espacio plausible. Léase así: con un impuesto del 20% "
  "y una ineficiencia fiscal del 35%, basta un θ del 3,5–4,1% para que el royalty domine — y los tramos ITEA permiten negociar hasta el 15–20%. "
  "El impuesto solo gana si el royalty está calibrado muy bajo, o si el canal fiscal fuera excepcionalmente eficiente."),
 s3tbl=[["θ* (acumulativo, despido a 55)","τ = 10%","τ = 20%","τ = 30%"],
        ["Ineficiencia fiscal 20%","2,2 – 2,6%","4,4 – 5,1%","6,5 – 7,7%"],
        ["Ineficiencia fiscal 35%","1,8 – 2,1%","3,5 – 4,1%","5,3 – 6,2%"],
        ["Ineficiencia fiscal 45%","1,5 – 1,8%","3,0 – 3,5%","4,5 – 5,3%"]],
 s4h="4 · El hallazgo central: la edad invierte el ranking",
 s4p=("Con arquitectura acumulativa, el θ* de indiferencia <b>cae</b> con la edad de despido: el trabajador desplazado a los 60 llega con "
  "25 años de derechos acumulados y le basta un θ del 1,5%; el desplazado a los 45 apenas acumuló y necesita un 8–9%. Con arquitectura plana "
  "ocurre exactamente lo contrario. Conclusión didáctica: <b>los dos sistemas no compiten, se complementan por edades</b>. El impuesto es el "
  "seguro natural del joven desplazado (su problema es de transición); el royalty acumulativo es el del senior (su problema es la expropiación "
  "de décadas de conocimiento). Un diseño híbrido — transferencia fiscal decreciente con la antigüedad y royalty creciente — dominaría a ambos, "
  "con el cruce en torno a los 48–52 años."),
 s5h="5 · La estructura impositiva de cada país mueve la frontera",
 s5p=("Tres parámetros nacionales deciden cuánto rinde cada sistema. <b>La cuña fiscal</b> (qué parte del coste laboral se queda por el camino): "
  "donde es alta (Bélgica 54%, Alemania, Francia), la base del impuesto es enorme — el mismo τ recauda un 40% más en Francia que en EE. UU. — "
  "pero el coste fiscal del despido también lo es. <b>La protección de base η₀</b>: en el bloque anglosajón la prestación pública repone menos "
  "de la mitad del sueldo (η₀ = 0,46), así que cualquier mecanismo añade más valor — y el royalty gana antes justo donde más falta hace. "
  "<b>La fiscalidad del capital</b>: el royalty tributa como ahorro (18% en EE. UU., 30% en Francia y Bélgica), y cada punto encarece el θ "
  "necesario. Resultado: el impuesto resiste mejor en el bloque continental de cuña alta; el royalty arrasa en el anglosajón. Para el Estado "
  "y el contribuyente no hay debate: el royalty cuesta entre un 26% y un 39% menos en los nueve países."),
 s6h="6 · La empresa: paga antes, pero existe una zona de acuerdo",
 s6p=("La perspectiva empresarial es la imagen en espejo. A flujos anuales parecidos (royalty del 10%: 14.620 €/año; impuesto del 20%: "
  "16.244 €/año), el valor presente del royalty <b>duplica</b> al del impuesto (152.700 € frente a 76.700 € por trabajador) — porque el impuesto "
  "se paga tarde y el royalty desde el primer año. Dos amortiguadores lo hacen contratable. Primero, la <b>financiación interna</b>: la wallet "
  "es un pasivo que la empresa remunera a IPC+spread, por debajo de su coste de deuda; para 1.000 trabajadores el pool alcanza 180 millones de € "
  "y recupera el 16% del coste. Segundo, y decisivo: cruzando la frontera de la empresa (θ máximo aceptable: 5,0% con τ=20%) con la del trabajador "
  "(θ mínimo: 3,7%) aparece una <b>zona de contratación</b> — θ entre 3,7% y 5,0% — donde ambos prefieren el royalty al impuesto. Y la zona se "
  "ensancha con τ: <b>el impuesto no es la alternativa al royalty, es la amenaza creíble que lo hace negociable</b>."),
 s7h="7 · Externalidades: qué corrige cada sistema y qué riesgos crea",
 s7a_t="Lo que el royalty corrige mejor", s7a=["La externalidad de demanda: mantiene renta y consumo sin perder el 20–45% en el canal fiscal.",
  "La recaudación evaporada: el Estado grava el flujo durante 30 años, no solo tras el despido.",
  "El atesoramiento de conocimiento: pagar por la transferencia de CI elimina el incentivo a ocultarlo (el impuesto incentiva lo contrario).",
  "El ciclo político: es contractual; sobrevive a los presupuestos anuales."],
 s7b_t="Los riesgos que el royalty debe gestionar", s7b=["Concentración de riesgo «Enron»: empleo, ahorro y crédito en la misma empresa que reestructura → fondo de garantía obligatorio.",
  "Aceleración: con los derechos ya devengados, despedir sale marginalmente más barato → devengo condicionado a permanencia.",
  "Desintermediación: un pool nacional de 20.000–30.000 M€ fuera de la supervisión bancaria exige transparencia regulatoria.",
  "Infradeclaración del valor V: requiere auditabilidad (metadatos de uso, atribución Shapley)."],
 s8h="8 · Conclusión: cuándo es óptimo cada sistema",
 verdA_t="El impuesto pigouviano es óptimo cuando…", verdA=["θ negociado por debajo del 2–4% (suelo de tramo)","El desplazado es joven o de baja antigüedad (< 12 años de CI)","La ocupación está bajo el percentil 50 ITEA (único instrumento universal)","País de cuña fiscal y fiscalidad del capital altas (Bélgica, Francia)","El canal fiscal es excepcionalmente eficiente (i ≤ 20%) y la afectación creíble"],
 verdB_t="El royalty acumulativo es óptimo cuando…", verdB=["θ ≥ 4–5% (cualquier tramo medio-alto ITEA)","Carrera acumulada ≥ 15 años; desplazados senior (≥ 50–55)","País de protección pública débil (EE. UU., R. Unido, Canadá)","Fiscalidad del capital moderada (≤ 22%: España, bloque anglosajón)","Siempre, desde la óptica del Estado y del contribuyente (26–39% más barato)"],
 final=("La recomendación de diseño que se deriva de la simulación: legislar el impuesto como régimen subsidiario (τ ≥ 20%) y permitir el "
  "descuelgue hacia royalties acumulativos negociados dentro de la zona de contratación, con garantía de insolvencia obligatoria, una fracción "
  "del depósito destinada a cotización de pensiones, y el spread de financiación interna como variable de reparto en convenio."),
 gloss_h="Glosario rápido",
 gloss=[("wᴵ","Coste laboral total: salario bruto + cotización empresarial. Es la base del impuesto y la referencia del valor V."),
  ("V","Flujo anual del activo algorítmico atribuible al trabajador: V = κ·wᴵ."),
  ("Vintage","La «cosecha» de derechos generada por los proyectos de un año; decae un 15% anual (vida media ≈ 6,7 años)."),
  ("Wallet","Cuenta personal custodiada donde se acumulan los derechos en tokens; tres destinos: depósito IPC, financiación interna (IPC+spread) o retirada."),
  ("i","Ineficiencia del canal fiscal: parte de la recaudación perdida en administración y peso muerto (20–45%)."),
  ("η₀","Recuperación de renta sin ningún mecanismo: lo que la prestación pública repone por sí sola (≈ 0,46–0,56 según país)."),
  ("Zona de contratación","Intervalo de θ donde trabajador y empresa prefieren ambos el royalty al impuesto: [3,7%, 5,0%] con τ = 20%.")],
 caveats=("Notas metodológicas: fiscalidad nacional paramétrica aproximada (2026); sistemas de desempleo simplificados (prestación bienal topada + "
  "asistencial); perfil de referencia P94/κ=1,8; términos reales con descuento del 3%; percentiles ITEA del ejemplo ilustrativos. La comparación de "
  "ciclo vital incluye la prefinanciación de la wallet, que la empresa paga durante la carrera: el royalty no es más barato en coste total — es mejor "
  "en sincronización. Resultados reproducibles con el motor del Simulador ITEA (fronteras.py, modelo.py, acumulativo.py)."),
 figc=["Fig. 1 — Renta del trabajador y wallet, 35→65 años.","Fig. 2 — Frontera θ* por país, τ e ineficiencia.",
  "Fig. 3 — θ* según la edad de despido y la arquitectura.","Fig. 4 — Cuña fiscal, η₀ y fiscalidad del capital por país.",
  "Fig. 5 — Coste anual para la empresa y zona de contratación."],
),
"en": dict(
 lang="en", title="Pigouvian tax or intellectual-capital royalties",
 subtitle="Which system protects better against agentic-AI displacement? A didactic simulation report",
 meta="ITEA Framework · Paper 8B (A. García-Lluis Valencia) · Forbes Global 2000 calibration · June 2026",
 s1h="1 · What is being compared",
 boxA_t="System A — Pigouvian tax", boxA=("A firm that replaces a worker with an AI agent pays a tax (a share τ of the labour cost it "
  "saves). The State collects that money and redistributes it to the displaced worker as an annual transfer. It is an <b>ex post</b> mechanism "
  "(it exists only after dismissal) and a <b>fiscal</b> one (it runs through the public administration, which loses 20–45% along the way to "
  "administration and deadweight)."),
 boxB_t="System B — Royalties for IC transfer", boxB=("The worker receives each year a share θ of the value of the algorithmic asset their "
  "knowledge helped create: a payment for the <i>transfer of their intellectual capital</i>. Rights accumulate over the career (each project "
  "generates a “vintage” that decays 15% per year) and are deposited as tokens in a custodied <b>wallet</b>, which can earn CPI, finance company "
  "projects at CPI+spread, or be withdrawn. It is an <b>ex ante</b> mechanism (it accrues while working) and a <b>contractual</b> one (≈1% "
  "administration cost)."),
 keyt="Five variables to read this report",
 keys=[("θ (theta)","The share of the algorithmic asset flow paid to the worker. This is the negotiated variable. ITEA brackets: 0.25–15% (percentiles 50–95) and 5–20% (Top 20)."),
  ("τ (tau)","The Pigouvian tax rate on saved labour cost. The literature places it between 10% and 30%."),
  ("η (eta)","The income recovery rate: what fraction of net salary the worker keeps after dismissal. η = 1 means full recovery; with no mechanism, η ≈ 0.5."),
  ("κ (kappa)","How many times labour cost the algorithmic asset is worth (V = κ·wᴵ). Calibrated with profit per employee of the world's 2,000 largest firms: 1.3 (retail) to 2.2 (banking)."),
  ("θ* (frontier)","The indifference θ: below it the worker prefers the tax; above it, the royalty. The whole report revolves around where this frontier lies.")],
 s2h="2 · The full picture: from age 35 to 65",
 s2p=("The figure shows a Spanish financial analyst (ITEA percentile 94, €77,500 gross) displaced at 55. The grey line is life without "
  "automation. Blue is the Pigouvian system: nothing changes until dismissal; afterwards the fiscal transfer restores part of the income. "
  "Green is the cumulative royalty system: for 20 years IC rights accumulate in the wallet (shaded area), which reaches dismissal with about "
  "€270,000 — pre-funded self-insurance that, together with the decaying royalties, sustains income better than the transfer. The key is not "
  "that the royalty pays more: it pays <b>when the knowledge transfer happens</b>, not when the dismissal does."),
 s3h="3 · The θ* frontier: how much royalty it takes to beat the tax",
 s3p=("For every country and tax configuration we compute the θ* above which the worker is better off with royalties. The frontier turns out "
  "narrow and low: between 1.5% and 7.7% across the entire plausible space. Read it like this: with a 20% tax and 35% fiscal inefficiency, a θ "
  "of 3.5–4.1% suffices for the royalty to dominate — and the ITEA brackets allow negotiating up to 15–20%. The tax only wins if the royalty is "
  "calibrated very low, or if the fiscal channel were exceptionally efficient."),
 s3tbl=[["θ* (cumulative, dismissal at 55)","τ = 10%","τ = 20%","τ = 30%"],
        ["Fiscal inefficiency 20%","2.2 – 2.6%","4.4 – 5.1%","6.5 – 7.7%"],
        ["Fiscal inefficiency 35%","1.8 – 2.1%","3.5 – 4.1%","5.3 – 6.2%"],
        ["Fiscal inefficiency 45%","1.5 – 1.8%","3.0 – 3.5%","4.5 – 5.3%"]],
 s4h="4 · The central finding: age reverses the ranking",
 s4p=("Under the cumulative architecture, the indifference θ* <b>falls</b> with dismissal age: a worker displaced at 60 arrives with 25 years "
  "of accrued rights and needs only θ = 1.5%; one displaced at 45 has barely accumulated and needs 8–9%. Under the flat architecture the "
  "opposite happens. The didactic conclusion: <b>the two systems do not compete — they complement each other across ages</b>. The tax is the "
  "natural insurance of the young displaced worker (a transition problem); the cumulative royalty is the senior's (an expropriation-of-decades "
  "problem). A hybrid design — a fiscal transfer decreasing with tenure plus a royalty increasing with it — would dominate both, crossing "
  "around ages 48–52."),
 s5h="5 · Each country's tax structure moves the frontier",
 s5p=("Three national parameters decide how much each system delivers. <b>The tax wedge</b> (how much of labour cost never reaches the worker): "
  "where it is high (Belgium 54%, Germany, France) the tax base is huge — the same τ collects 40% more in France than in the US — but so is the "
  "fiscal cost of each dismissal. <b>Baseline protection η₀</b>: in the Anglo bloc, public benefits replace less than half the salary (η₀ = 0.46), "
  "so any mechanism adds more value — and the royalty wins earlier precisely where it is most needed. <b>Capital taxation</b>: royalties are taxed "
  "as savings income (18% in the US, 30% in France and Belgium), and every point raises the required θ. Result: the tax resists best in the "
  "high-wedge continental bloc; the royalty sweeps the Anglo bloc. For the State and the taxpayer there is no contest: the royalty costs 26–39% "
  "less in all nine countries."),
 s6h="6 · The firm: it pays earlier, but a bargaining zone exists",
 s6p=("The firm's perspective is the mirror image. With similar annual flows (10% royalty: €14,620/yr; 20% tax: €16,244/yr), the present value "
  "of the royalty <b>doubles</b> that of the tax (€152,700 vs €76,700 per worker) — because the tax is paid late and the royalty from year one. "
  "Two buffers make it contractible. First, <b>internal financing</b>: the wallet is a liability the firm remunerates at CPI+spread, below its "
  "cost of debt; for 1,000 workers the pool reaches €180m and recovers 16% of the cost. Second, and decisive: crossing the firm's frontier "
  "(max acceptable θ: 5.0% at τ=20%) with the worker's (min θ: 3.7%) reveals a <b>contracting zone</b> — θ between 3.7% and 5.0% — where both "
  "prefer the royalty to the tax. And the zone widens with τ: <b>the tax is not the alternative to the royalty; it is the credible threat that "
  "makes it negotiable</b>."),
 s7h="7 · Externalities: what each system corrects and what risks it creates",
 s7a_t="What the royalty corrects better", s7a=["The demand externality: it sustains income and consumption without losing 20–45% in the fiscal channel.",
  "Evaporated revenue: the State taxes the flow for 30 years, not only after dismissal.",
  "Knowledge hoarding: paying for IC transfer removes the incentive to hide it (the tax incentivises the opposite).",
  "The political cycle: it is contractual; it survives annual budgets."],
 s7b_t="The risks the royalty must manage", s7b=["“Enron” risk concentration: job, savings and credit in the same restructuring firm → mandatory guarantee fund.",
  "Acceleration: with rights already accrued, dismissal becomes marginally cheaper → accrual conditional on continued employment.",
  "Disintermediation: a national pool of €20–30bn outside banking supervision requires regulatory transparency.",
  "Under-declaration of V: requires auditability (usage metadata, Shapley attribution)."],
 s8h="8 · Conclusion: when each system is optimal",
 verdA_t="The Pigouvian tax is optimal when…", verdA=["θ negotiated below 2–4% (bracket floor)","The displaced worker is young or low-tenure (< 12 years of IC)","The occupation is below the 50th ITEA percentile (the only universal instrument)","High tax-wedge, high capital-tax country (Belgium, France)","The fiscal channel is exceptionally efficient (i ≤ 20%) with credible earmarking"],
 verdB_t="The cumulative royalty is optimal when…", verdB=["θ ≥ 4–5% (any mid-to-high ITEA bracket)","Accumulated career ≥ 15 years; senior displaced workers (≥ 50–55)","Weak public protection country (US, UK, Canada)","Moderate capital taxation (≤ 22%: Spain, Anglo bloc)","Always, from the State's and the taxpayer's perspective (26–39% cheaper)"],
 final=("The design recommendation that follows from the simulation: legislate the tax as a subsidiary regime (τ ≥ 20%) and allow opting out "
  "into cumulative royalties negotiated within the contracting zone, with a mandatory insolvency guarantee, a fraction of the deposit allocated "
  "to pension contributions, and the internal-financing spread as the distribution variable in collective bargaining."),
 gloss_h="Quick glossary",
 gloss=[("wᴵ","Total labour cost: gross salary + employer social contributions. The tax base and the reference for V."),
  ("V","Annual flow of the algorithmic asset attributable to the worker: V = κ·wᴵ."),
  ("Vintage","The “harvest” of rights generated by one year's projects; decays 15% per year (mean life ≈ 6.7 years)."),
  ("Wallet","Custodied personal account where rights accumulate as tokens; three destinations: CPI deposit, internal financing (CPI+spread) or withdrawal."),
  ("i","Fiscal channel inefficiency: the share of revenue lost to administration and deadweight (20–45%)."),
  ("η₀","Income recovery with no mechanism: what public benefits replace on their own (≈ 0.46–0.56 by country)."),
  ("Contracting zone","θ interval where worker and firm both prefer the royalty to the tax: [3.7%, 5.0%] at τ = 20%.")],
 caveats=("Methodological notes: approximate parametric national taxation (2026); simplified unemployment systems (capped two-year benefit + "
  "assistance); reference profile P94/κ=1.8; real terms with 3% discounting; ITEA percentiles in the example are illustrative. The lifetime "
  "comparison includes the wallet pre-funding, paid by the firm during the career: the royalty is not cheaper in total cost — it is better in "
  "timing. Results reproducible with the ITEA Simulator engine (fronteras.py, modelo.py, acumulativo.py)."),
 figc=["Fig. 1 — Worker income and wallet, ages 35→65.","Fig. 2 — θ* frontier by country, τ and inefficiency.",
  "Fig. 3 — θ* by dismissal age and architecture.","Fig. 4 — Tax wedge, η₀ and capital taxation by country.",
  "Fig. 5 — Annual firm cost and the contracting zone."],
),
}

CSS = """
@page { size: A4; margin: 18mm 16mm 16mm 16mm;
  @bottom-center { content: counter(page) " / " counter(pages); font-family:'DejaVu Sans'; font-size:7.5pt; color:#8A949C; } }
* { box-sizing: border-box; }
body { font-family:'DejaVu Sans', sans-serif; font-size:9.3pt; line-height:1.45; color:#16242F; margin:0; }
.cover { background:#16242F; color:#fff; padding:26mm 14mm 16mm; margin:-18mm -16mm 8mm; }
.cover h1 { font-family:'DejaVu Serif', serif; font-size:21pt; line-height:1.2; margin:0 0 4mm; }
.cover .sub { font-size:11pt; color:#C9D4DC; margin-bottom:8mm; }
.cover .meta { font-size:8pt; color:#8FA0AC; border-top:0.4pt solid #3A4A57; padding-top:3mm; }
.tag { display:inline-block; background:#1E7A52; color:#fff; font-size:7.5pt; padding:1pt 6pt; border-radius:2pt; margin-bottom:5mm; letter-spacing:1pt;}
h2 { font-family:'DejaVu Serif', serif; font-size:12.5pt; color:#16242F; border-bottom:1.6pt solid #16242F; padding-bottom:1.5pt; margin:7mm 0 3mm; }
p { margin:0 0 2.6mm; text-align:justify; }
.twocol { display:flex; gap:4mm; margin:3mm 0; }
.box { flex:1; border:0.5pt solid #D7DEE4; border-radius:2.5pt; padding:3mm; background:#F8FAFB; }
.box.blue { border-top:2.5pt solid #2456A6; } .box.green { border-top:2.5pt solid #1E7A52; }
.box h3 { font-size:9.5pt; margin:0 0 1.6mm; } .box.blue h3{color:#2456A6;} .box.green h3{color:#1E7A52;}
.box p { font-size:8.6pt; margin:0; }
.keys { margin:2mm 0; } .keys td { font-size:8.4pt; padding:1.3mm 2mm; border-bottom:0.4pt solid #E4E9ED; vertical-align:top;}
.keys td:first-child { font-family:'DejaVu Sans Mono'; font-weight:bold; white-space:nowrap; color:#16242F; width:18mm;}
img.fig { width:100%; margin:1.5mm 0 0.5mm; }
.figcap { font-size:7.6pt; color:#5C6B76; margin-bottom:3mm; }
table.res { border-collapse:collapse; width:100%; margin:2mm 0 3mm; }
table.res th, table.res td { border:0.4pt solid #C8D1D8; font-size:8.4pt; padding:1.4mm 2mm; text-align:center; }
table.res th { background:#16242F; color:#fff; font-weight:normal; }
table.res td:first-child { text-align:left; background:#F2F5F7; }
ul { margin:1mm 0 2mm; padding-left:4.5mm; } li { font-size:8.6pt; margin-bottom:1mm; }
.verd { display:flex; gap:4mm; } 
.verd .box.blue li::marker{color:#2456A6;} .verd .box.green li::marker{color:#1E7A52;}
.final { background:#EFF5F1; border-left:2.5pt solid #1E7A52; padding:2.5mm 3mm; font-size:9pt; margin:3mm 0; }
.gloss td { font-size:8.2pt; padding:1.2mm 2mm; border-bottom:0.4pt solid #E4E9ED; vertical-align:top;}
.gloss td:first-child { font-family:'DejaVu Sans Mono'; font-weight:bold; white-space:nowrap; width:24mm;}
.caveats { font-size:7.6pt; color:#5C6B76; border-top:0.5pt solid #C8D1D8; padding-top:2mm; margin-top:4mm; text-align:justify;}
.pagebreak { page-break-before: always; }
"""

def tbl(rows):
    out = "<table class='res'><tr>" + "".join(f"<th>{c}</th>" for c in rows[0]) + "</tr>"
    for r in rows[1:]:
        out += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    return out + "</table>"

def build(lang):
    c = C[lang]; F = [img64(f"/home/claude/sim/pdf_f{i}_{lang}.png") for i in range(1,6)]
    keys = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k,v in c["keys"])
    gloss = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k,v in c["gloss"])
    lis = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    html = f"""<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>
<div class='cover'><div class='tag'>ITEA · SIMULACIÓN / SIMULATION</div>
 <h1>{c['title']}</h1><div class='sub'>{c['subtitle']}</div><div class='meta'>{c['meta']}</div></div>

<h2>{c['s1h']}</h2>
<div class='twocol'><div class='box blue'><h3>{c['boxA_t']}</h3><p>{c['boxA']}</p></div>
<div class='box green'><h3>{c['boxB_t']}</h3><p>{c['boxB']}</p></div></div>
<p><b>{c['keyt']}</b></p><table class='keys'>{keys}</table>

<h2>{c['s2h']}</h2><p>{c['s2p']}</p>
<img class='fig' src='{F[0]}'/><div class='figcap'>{c['figc'][0]}</div>

<div class='pagebreak'></div>
<h2>{c['s3h']}</h2><p>{c['s3p']}</p>
{tbl(c['s3tbl'])}
<img class='fig' src='{F[1]}'/><div class='figcap'>{c['figc'][1]}</div>

<h2>{c['s4h']}</h2><p>{c['s4p']}</p>
<img class='fig' src='{F[2]}'/><div class='figcap'>{c['figc'][2]}</div>

<div class='pagebreak'></div>
<h2>{c['s5h']}</h2><p>{c['s5p']}</p>
<img class='fig' src='{F[3]}'/><div class='figcap'>{c['figc'][3]}</div>

<h2>{c['s6h']}</h2><p>{c['s6p']}</p>
<img class='fig' src='{F[4]}'/><div class='figcap'>{c['figc'][4]}</div>

<div class='pagebreak'></div>
<h2>{c['s7h']}</h2>
<div class='twocol'><div class='box green'><h3>{c['s7a_t']}</h3><ul>{lis(c['s7a'])}</ul></div>
<div class='box blue'><h3>{c['s7b_t']}</h3><ul>{lis(c['s7b'])}</ul></div></div>

<h2>{c['s8h']}</h2>
<div class='verd'><div class='box blue'><h3>{c['verdA_t']}</h3><ul>{lis(c['verdA'])}</ul></div>
<div class='box green'><h3>{c['verdB_t']}</h3><ul>{lis(c['verdB'])}</ul></div></div>
<div class='final'>{c['final']}</div>

<h2>{c['gloss_h']}</h2><table class='gloss'>{gloss}</table>
<div class='caveats'>{c['caveats']}</div>
</body></html>"""
    out = f"/home/claude/sim/Informe_ITEA_{lang.upper()}.pdf"
    HTML(string=html).write_pdf(out)
    return out

for lang in ("es","en"):
    print(build(lang))
