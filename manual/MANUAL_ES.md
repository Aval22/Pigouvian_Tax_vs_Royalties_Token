# Manual metodológico — v1.0

**Pigouvian Tax vs Royalties Token** · Simulador comparado de mecanismos de compensación frente al desplazamiento por IA agéntica
Marco: ITEA Framework · Paper 8B "El derecho residual tokenizado" (A. García-Lluis Valencia, 2026)

---

## 1. Propósito

Este proyecto compara cuantitativamente dos mecanismos de respuesta al desplazamiento laboral por IA agéntica: el **impuesto pigouviano** sobre la automatización (Falk-Tsoukalas) y el **derecho residual tokenizado** — un royalty por la transferencia de capital intelectual (CI) del trabajador al activo algorítmico de la empresa, calibrado por exposición ocupacional (ITEA/OAXI). El simulador evalúa ambos sistemas para cuatro actores (trabajador, empresa, Estado, contribuyente) en nueve países, sobre un ciclo vital de 35 a 65 años.

## 2. Marco teórico

El impuesto pigouviano corrige una **externalidad de demanda**: la firma que automatiza captura el 100% del ahorro de costes pero solo sufre 1/N del daño que la destrucción de salarios causa sobre la demanda agregada. El tipo óptimo es τ\* = f·(1−1/N). El derecho residual parte del diagnóstico de la **expropiación algorítmica** (Paper 8B): la cristalización del conocimiento tácito del trabajador (Polanyi; Nonaka-SECI) en activos algorítmicos de la firma constituye una transferencia de capital no remunerada que el contrato industrial de trabajo no contempla (Williamson; Hodgson). El royalty θ·V es la contraprestación de esa transferencia; sus dos canales formales son la condición de retención (ec. 8 del paper) y la tasa de recuperación de renta η (ec. 9).

## 3. Arquitectura del simulador

Flujo: **país → ocupación (Title O*NET, percentil ITEA) → salario bruto (ventana emergente) → módulo pigouviano ‖ módulo royalties → veredicto por actor + progresión temporal + interpretación generada**. Todos los parámetros numéricos son deslizadores continuos dentro de su horquilla; los valores "base" son solo la posición inicial. Cálculo en términos reales (descuento 3%).

## 4. Módulo salarial por país

Cada país se parametriza con: escala de IRPF por tramos, cotización del trabajador (tipo y tope), **cotización empresarial** (que define el coste laboral total wᴵ = bruto + cotización patronal, base del impuesto y referencia de V), fiscalidad del ahorro/capital (grava el royalty), imposición efectiva al consumo (canal fiscal de la demanda), tope de la prestación contributiva y nivel asistencial, y población de contribuyentes. Fuentes de validación: calculadoras seleccionadas por país (Cinco Días ES; code.travail.gouv.fr FR — única oficial con coste empleador; Sparkasse DE; CalcolaStipendioNetto/Stipendee IT; SD Worx BE; Doutor Finanças/Literacia PT; The Salary Calculator/MoneyHelper UK; ADP/SmartAsset US; Wealthsimple CA) con ancla de comparabilidad en **OECD Taxing Wages**.

## 5. Módulo pigouviano — fundamento de cada variable

| Variable | Horquilla (defecto) | Fundamento |
|---|---|---|
| τ — tipo sobre el ahorro laboral | 0,5–50% (20%) | Slider libre con zona de literatura 10–30% marcada. Dentro de 0,5–50% el impuesto es redistributivo, no preventivo: la firma sigue ahorrando ≥50% del coste laboral. |
| N — estructura competitiva | 2–60 (sectorial) | N efectivo = 1/HHI, calibrado con cuotas de ventas del Forbes Global 2000 por industria. Determina la fracción del daño de demanda que la firma ignora: (1−1/N). |
| f — intensidad de la externalidad | 0,10–0,40 (derivada) | f ≈ (PMC_trabajadores − PMC_capital) × multiplicador × traslación ≈ 0,2–0,3. En modo libre se muestra la f implícita = τ/(1−1/N) como control de coherencia. |
| i — ineficiencia del canal fiscal | 5–45% (20%) | Suelo: coste administrativo de programas activos (Card-Kluve-Weber, 5–15%). Tramos 20/35/45%: coste marginal de los fondos públicos (Ballard et al.; Feldstein). |
| α — afectación de la recaudación | 0–100% (100%) | α=1: afectación íntegra a compensación. α<1 modela captura presupuestaria; el impuesto se vuelve fuente de ingresos en la medida en que deja de compensar. |
| D — duración de la transferencia | 1–10 años (10) | De espejo de la prestación (2) a renta puente hasta jubilación. |
| t_tr — fiscalidad de la transferencia | 0–45% (15%) | De exenta (estilo indemnización) a rendimiento del trabajo pleno. |
| λ_t — take-up | 70–100% | Non-take-up documentado de los programas condicionados (15–30%). |
| e — erosión de la base | 0–30% | Elusión definicional ("¿qué cuenta como robot/agente?"), crítica estándar al robot tax (Abbott-Bogenschneider). |

## 6. Módulo de royalties — fundamento de cada variable

| Variable | Horquilla (defecto) | Fundamento |
|---|---|---|
| θ — derecho residual, tramo P50–P95 | 0,25–15% (5%) | Tramos ITEA fusionados por decisión de diseño v1.0; escala logarítmica recomendada. Marca en rojo bajo la condición de participación. |
| θ — Top 20 OAXI | 5–20% (12,5%) | Banderín de sobrecompensación si η>1 (subautomatización, Corolario 2 invertido). |
| κ_V — multiplicador del activo | 1,0–4,0 (sectorial) | V = κ·wᴵ. Calibrado: κ ≈ 1 + beneficio_por_empleado/wᴵ con medianas Forbes 2024 (comercio 1,3 … banca 2,2); techo = ventas/empleado÷wᴵ como cota de negociación. |
| Arquitectura | plana / **acumulativa** | La acumulativa devenga derechos por *vintages* anuales: paga cuando ocurre la transferencia de CI, no cuando ocurre el despido. Resultado v1.0: baja el θ\* de dominancia y lo hace decreciente con la edad. |
| δ — decaimiento del vintage | 10–25% (15%) | Pérdida anual de valor de la cosecha de cada proyecto. δ=15% ⇒ vida media geométrica ≈ 6,7 años, consistente con vida de proyecto de 6 años. Proxy sectorial: Δ intensidad de capital del panel Forbes 2014–2024. |
| Años de carrera acumulada | 5–35 (20) | Rampa 1−(1−δ)^s hacia el flujo estacionario θ·V (96% a los 20 años). Bajo ~7 años el acumulativo paga menos que el plano. |
| Wallet: depósito IPC | 0–100% (50%) | Tokens custodiados indexados a inflación: 0% real, sin riesgo de mercado, con riesgo de contraparte. |
| Wallet: financiación interna | complemento | El saldo presta a proyectos de la empresa como producto financiero interno (canal Pensionsrückstellungen/Genussschein, §3.1.bis del paper). |
| Spread de financiación | IPC+0,5 – IPC+4% (2%) | Acotado entre el depósito y el coste de deuda real de la firma (~3%): la llave de reparto del excedente financiero. Aviso de concentración si la asignación interna supera el 50% (riesgo Enron-401k). |
| Retirada anual | 0–100% (0%) | Rescate en carrera; erosiona el autoseguro. Fiscalidad diseñable para desincentivar sin prohibir. |
| Fiscalidad del royalty | RCM del país | Tributa como renta del ahorro en el devengo. Cuña clave: eleva el θ de recuperación plena ~26% sobre el teórico bruto. |
| Garantía en insolvencia | fondo tipo FOGASA / segregación | Condición de diseño, no opción: el evento asegurado correlaciona con la insolvencia. |

## 7. Calibración empresarial (Forbes Global 2000)

Fuente: listas 2014 (xls original), 2019 y 2024 (panel; la hoja 2024 incluye **empleados e industria**: 1.943 firmas válidas). Productos: ratios mediana de ventas y beneficio por empleado por sector armonizado (24 sectores), márgenes, HHI y N efectivo por industria, y panel 2014→2024 de intensificación de capital (proxy de velocidad de automatización). Limitaciones: dólares corrientes, universo truncado a grandes cotizadas (κ es cota superior para pymes), EBITDA no disponible (complementar con márgenes Damodaran).

## 8. Motor de desplazamiento y pensiones

Despido a la edad configurada; ciclo: prestación contributiva 24 meses topada por país → asistencial → recolocación con hazard anual (15% seniors) y penalización salarial (28%). Memo de pensiones (caso ES): erosión de base reguladora ≈ 20% (≈ 90.000 € NPV vitalicio) que **ningún** mecanismo repara — motiva la opción de destinar parte del depósito a convenio especial.

## 9. Outputs derivados (siempre visibles)

θ_min de retención (ec. 8): (wᴵ−(F+K)·r)/V. θ_η1 bruto y **neto** de la cuña fiscal. **Condición de participación**: θ ≥ τ·wᴵ·(1−i)·α/V — el suelo que hace el royalty preferido al impuesto vigente. f implícita. Banderín η>1.

## 10. Resultados clave v1.0

(1) La frontera θ\* del trabajador es estrecha: 1,5–7,7% en todo el espacio plausible; con θ≥5% el royalty acumulativo domina en los 9 países. (2) **La edad invierte el ranking**: θ\* cae de ~8,5% (despido a 45) a ~1,6% (a 60) con arquitectura acumulativa, y sube con la plana ⇒ los sistemas se complementan por cohortes; óptimo híbrido con cruce en 48–52 años. (3) Tres bloques de países: continental (cuña alta: impuesto potente pero caro), anglosajón (η₀=0,46: el royalty gana antes y donde más falta hace), salarios bajos (η₀ alto: ambos añaden menos). (4) Para Estado y contribuyente el royalty cuesta 26–39% menos con afectación íntegra. (5) Para la empresa el royalty es **más caro en valor presente** (paga antes) pero existe una **zona de contratación** θ∈[3,7%, 5,0%] a τ=20% donde ambas partes lo prefieren — el impuesto es la amenaza creíble que la abre; la financiación interna recupera ~16% del coste.

## 11. Limitaciones v1.0

Fiscalidad nacional paramétrica aproximada (validación fina pendiente contra las calculadoras seleccionadas); desempleo simplificado; percentiles ITEA del selector ilustrativos (sustituir por la serie ITEA v3.0); canal Weitzman (devengo sobre ingresos con ciclo) no simulado; sin equilibrio general (precios y salarios exógenos); comparación de ciclo vital con la advertencia de sincronización (la wallet la prefinancia la empresa).

## 12. Reproducibilidad

`src/modelo.py` (motor base ES) → `src/acumulativo.py` (vintages+wallet) → `src/fronteras.py` (9 países, rejillas θ\*) → `src/calibracion_forbes.py` (κ, HHI, panel) → `src/figs_pdf.py` + `src/informe_pdf.py` (informes PDF ES/EN). Datos en `data/`, figuras en `figures/`, dashboard en `docs/index.html` (GitHub Pages).
