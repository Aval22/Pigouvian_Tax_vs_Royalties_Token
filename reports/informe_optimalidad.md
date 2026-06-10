# Fronteras de optimalidad: ¿cuándo es óptimo el impuesto pigouviano y cuándo el pago de royalties?

**Método:** motor del Simulador ITEA portado a 9 países (fiscalidad aproximada 2026), barrido de τ ∈ {10, 20, 30%} × ineficiencia ∈ {20, 35, 45%} × edad de desplazamiento ∈ {45, 50, 55, 60} × arquitectura {plana, acumulativa}, con perfil de referencia analista financiero (ITEA P94, κ = 1,8, salario indexado por país). La frontera se expresa como **θ\*** — el derecho residual de indiferencia: por debajo de θ\*, el trabajador está mejor con el impuesto; por encima, con el royalty. Cifras en `fronteras_theta.csv`, `fronteras_edad.csv`, `estructura_pais.csv`; figuras 6–8. · Junio 2026

---

## 1. La frontera fundamental: θ\* es esencialmente proporcional a τ·(1−i)

El primer resultado ordena todo lo demás: como ambos flujos escalan con el coste laboral wᴵ, la frontera de indiferencia del trabajador es aproximadamente **θ\* ≈ τ·(1−i)·wᴵ/V**, corregida por la cuña fiscal del capital y la arquitectura. Con la configuración central (despido a 55, acumulativo), la tabla completa queda:

| θ\* (acumulativo, 55 años) | τ=10% | τ=20% | τ=30% |
|---|---|---|---|
| Ineficiencia 20% | 2,2–2,6% | 4,4–5,1% | 6,5–7,7% |
| Ineficiencia 35% | 1,8–2,1% | 3,5–4,1% | 5,3–6,2% |
| Ineficiencia 45% | 1,5–1,8% | 3,0–3,5% | 4,5–5,3% |

(El rango en cada celda recoge los 9 países: EE. UU. siempre en el extremo bajo, Bélgica y Francia en el alto.)

La lectura normativa es directa. **El pigouviano solo es óptimo para el trabajador cuando θ está calibrado por debajo de estas cifras** — y todas ellas caen en el tercio inferior de los sliders del simulador (0,25–15% / 5–20%). Con un θ de tramo medio razonable (≥ 5%), el royalty acumulativo domina al impuesto en cualquier combinación plausible de τ e ineficiencia, en los nueve países. El impuesto necesita simultáneamente ser muy generoso (τ = 30%), muy eficiente (i = 20%) y enfrentarse a un royalty raquítico (θ < 7,7%) para ganar. Inversamente, el royalty pierde con seguridad solo en la franja θ < 1,5–2%, que es precisamente la zona baja del tramo P50–P95 que tu horquilla del 0,25% permite — el simulador marcará en rojo esa franja con la condición de participación.

## 2. Estructura impositiva por país: tres determinantes, tres bloques

La fig. 8 muestra los tres parámetros estructurales que mueven la frontera país a país, y que el barrido cuantifica:

| País | Cuña fiscal (1−neto/wᴵ) | η₀ sin mecanismo | Fiscalidad del capital | θ\* (τ=20%, i=35%) | Coste fiscal S2 / S3 (NPV 10a) |
|---|---|---|---|---|---|
| Bélgica | **54,1%** | 0,55 | 30% | 4,1% | 185.536 / 121.899 € |
| Alemania | 50,7% | 0,52 | 26% | 3,9% | 170.348 / 116.150 € |
| Francia | 49,7% | 0,51 | 30% | 4,1% | 174.485 / 109.024 € |
| Italia | 49,5% | 0,51 | 26% | 3,9% | 131.429 / 88.244 € |
| España | 46,7% | 0,51 | 21% | 3,7% | 132.561 / 96.038 € |
| Portugal | 43,6% | **0,56** | 28% | 4,0% | 85.538 / 55.353 € |
| R. Unido | 32,2% | **0,46** | 20% | 3,6% | 80.999 / 49.593 £ |
| Canadá | 27,8% | 0,52 | 22% | 3,7% | 107.000 / 66.944 C$ |
| EE. UU. | **26,5%** | **0,46** | 18% | **3,5%** | 106.947 / 68.387 $ |

**Bloque continental (BE, FR, DE, IT, ES, PT).** La cuña fiscal alta tiene un efecto doble y contradictorio sobre el pigouviano. A favor: la base imponible es enorme (la cotización patronal del 27–42% infla wᴵ — el mismo τ del 20% recauda en Francia un 40% más por trabajador que en EE. UU.), así que el impuesto transfiere mucho. En contra: cada euro de salario destruido evapora también mucha recaudación, de modo que el **coste fiscal del escenario pigouviano es máximo justo donde el impuesto es más potente** (Bélgica: 185.500 € por trabajador, frente a 121.900 con royalties — un 34% menos). Además, la fiscalidad del capital alta (26–30%) muerde el royalty y empuja θ\* hacia arriba: por eso Bélgica y Francia son los países donde el impuesto resiste mejor. Síntesis continental: *el pigouviano es relativamente más competitivo, pero también relativamente más caro de sostener*.

**Bloque anglosajón (US, UK, CA).** Todo se invierte. La base pigouviana es pequeña (cotización patronal del 7,7–15%), la protección de base es mínima (η₀ = 0,46 en UK y US: la prestación británica de ~110 £/semana repone una fracción ínfima de estos salarios, y el subsidio asistencial estadounidense es cero), y la fiscalidad del capital baja (18–22%) abarata el royalty. Resultado: **θ\* mínimo (3,5–3,7%) y máxima ventaja relativa del sistema de royalties** — que además le cuesta al Estado un 36–39% menos. En estos países el royalty no solo gana antes: gana donde más falta hace, porque el suelo público que el desplazado pisa es más bajo.

**El caso portugués** ilustra el tercer determinante: con salarios bajos, el tope de la prestación deja de morder y η₀ sube a 0,56 — la protección pública existente ya repone más, así que *ambos* mecanismos añaden menos valor marginal. Generalización: la urgencia de cualquiera de los dos sistemas crece con el nivel salarial del perfil, porque los topes de prestación convierten los sistemas de desempleo europeos en regresivos por arriba.

## 3. La edad de desplazamiento: el hallazgo central del barrido

La fig. 7 contiene el resultado más importante del informe: **la edad invierte el ranking de los sistemas, y la arquitectura del royalty determina el sentido de la inversión.**

| θ\* (τ=20%, i=35%) | Despido a 45 | A 50 | A 55 | A 60 |
|---|---|---|---|---|
| Royalty **acumulativo** | 7,6–8,9% | 4,9–5,7% | 3,5–4,1% | **1,5–1,7%** |
| Royalty **plano** | **4,3–5,0%** | 5,3–6,3% | 7,5–8,8% | 7,5–8,8% |

Con arquitectura acumulativa, θ\* **cae** monótonamente con la edad: el desplazado a los 60 llega con 25 años de vintages y una wallet llena — le basta un θ del 1,5% para preferir el royalty. El desplazado a los 45 solo acumuló 10 años (el 80% del flujo estacionario, pero poca wallet) y afronta 20 años hasta la jubilación: necesita θ ≥ 8–9%, y la transferencia pigouviana —que no depende de la antigüedad— le resulta comparativamente mejor. Con arquitectura plana ocurre lo contrario: θ\* **sube** con la edad, porque el royalty plano paga solo durante la ventana post-despido, que se encoge (10 años a los 55, 5 a los 60) mientras la prestación pigouviana se encoge igual — el plano pierde su ventaja diferencial.

La consecuencia de diseño es elegante y publicable: **los dos sistemas no compiten, se complementan por cohortes de edad.** El pigouviano es el seguro natural del trabajador joven desplazado (sin capital intelectual acumulado que monetizar: su problema es de transición, no de expropiación); el royalty acumulativo es el seguro natural del trabajador senior (su problema es exactamente la expropiación de 20–30 años de CI cristalizado, y la wallet es su contravalor). Un diseño híbrido —transferencia fiscal decreciente con la antigüedad + royalty acumulativo creciente con ella— dominaría a cualquiera de los dos puros, y la frontera de cruce está en torno a los 48–52 años de edad de despido (12–17 años de antigüedad) en los nueve países.

## 4. Estado y contribuyente: el royalty domina sin excepción en esta configuración

Con afectación íntegra e ineficiencia ≥ 20%, el coste fiscal por trabajador del escenario royalty es entre un 26% (España) y un 39% (Reino Unido) inferior al pigouviano en los nueve países, por tres vías acumulativas: el Estado recauda la fiscalidad del capital sobre el royalty durante toda la carrera (no solo tras el despido), no soporta el peso muerto del canal fiscal, y la renta post-despido más alta devuelve más imposición al consumo. Para el contribuyente, eso se traduce en que la factura anual por contribuyente del pigouviano supera a la del royalty en todos los escenarios del barrido; la brecha crece con la cuña fiscal del país (máxima en Bélgica) y con la ineficiencia. La única configuración donde el Estado prefiere el impuesto es con afectación parcial (α < 1): si retiene parte de la recaudación para caja general, el pigouviano se convierte en fuente neta de ingresos — a costa, claro, de dejar de cumplir su función compensatoria (la Limitación 3 del paper, ahora cuantificada como trade-off α).

## 5. Tabla síntesis de escenarios

**El impuesto pigouviano es el sistema óptimo cuando** se combinan varias de estas condiciones: θ calibrado por debajo del 2–4% (tramo bajo de P50–P95); desplazados jóvenes o de baja antigüedad (< 12 años de acumulación de CI); arquitectura de royalty plana en lugar de acumulativa; países de cuña fiscal alta y fiscalidad del capital alta (Bélgica, Francia) donde la base imponible patronal maximiza la transferencia; canal fiscal excepcionalmente eficiente (i ≤ 20%) con afectación íntegra creíble; y ocupaciones bajo el percentil 50 ITEA, fuera del ámbito de θ, donde es el único instrumento disponible. Su ventaja estructural irreductible: no depende de la antigüedad ni del θ negociado — es el mecanismo de *último recurso* universal.

**El pago de royalties es el sistema óptimo cuando**: θ ≥ 4–5% (cualquier calibración de tramo medio-alto); arquitectura acumulativa con ≥ 15 años de carrera; desplazados senior (≥ 50–55 años), que son precisamente la población de mayor daño (η₀ ≈ 0,5) y peor recolocación; países de cuña fiscal baja y protección pública débil (EE. UU., R. Unido, Canadá), donde llena un vacío que el Estado no cubre; fiscalidad del capital moderada (≤ 22%: España, EE. UU., R. Unido, Canadá); y siempre que la perspectiva sea la del Estado o el contribuyente, donde domina sin excepción en el barrido. Sus condiciones de fallo son igual de claras: θ bajo el suelo de participación, carreras cortas, y ocupaciones < P50.

## 6. Advertencias metodológicas

La frontera θ\* es la indiferencia del **trabajador**; las fronteras del Estado y la empresa son distintas (la empresa es indiferente en θ·κ = τ, el Estado prefiere royalty casi siempre con α = 1). La comparación de ciclo vital incluye la prefinanciación de la wallet, que la empresa paga durante la carrera fuera de la ventana de despido: el royalty no es más barato en coste total, es mejor en *sincronización* (es un seguro, no un regalo). La fiscalidad por país es paramétrica aproximada (pendiente de validación fina con las calculadoras seleccionadas) y los sistemas de desempleo están simplificados a tope contributivo bienal + asistencial. El perfil de referencia es P94/κ=1,8; perfiles de κ mayor (banca, 2,2) desplazan todas las θ\* a la baja proporcionalmente, y viceversa.

*Archivos: `fronteras.py`, `fronteras_theta.csv`, `fronteras_edad.csv`, `estructura_pais.csv`, `fig6_frontera_pais.png`, `fig7_frontera_edad.png`, `fig8_estructura_pais.png`.*
