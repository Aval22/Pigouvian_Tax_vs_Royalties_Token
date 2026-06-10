# Simulación comparada: impuesto pigouviano vs. derecho residual tokenizado (θ·V)

**Marco:** Paper 8B v1.7 (García-Lluis Valencia, 2026), ecs. (5)–(9) y calibración §3.3 · **Horizonte:** 10 años (edad 55 → jubilación a los 65) · **Fecha:** junio 2026

---

## 1. Diseño de la simulación

Se comparan cuatro escenarios para tres perfiles profesionales españoles desplazables por IA agéntica a los 55 años, con los datos netos de la calculadora de Cinco Días aportados como input. El escenario S0 (continuidad) es el contrafactual sin automatización. S1 simula la sustitución agéntica sin política correctiva. S2 aplica el impuesto pigouviano de Falk-Tsoukalas como un tipo τ = 20% sobre el ahorro de coste laboral (τ* = f·(1−1/N) con N = 10), recaudado por el Estado con un coste administrativo del 10% (punto medio Card-Kluve-Weber) y redistribuido al desplazado como anualidad. S3 aplica el derecho residual tokenizado con θ_j calibrado por tramo OAXI según §3.3: la firma paga θ_j·V_j al trabajador, que tributa como rendimiento de capital mobiliario (19–28%).

El valor del activo agéntico se parametriza como V_j = κ·wᴵ con κ = 1,5 en el caso base (wᴵ = coste laboral total: bruto + 31% de cotización empresarial sobre base topada en 60.000 €). El ciclo de desempleo español se modela completo: prestación contributiva 24 meses topada (1.225 €/mes sin hijos; 1.575 €/mes con dos hijos), subsidio para mayores de 52 años (80% IPREM = 480 €/mes) hasta la recolocación o los 65, hazard anual de reempleo del 15% (seniors) con penalización salarial del 28%, y erosión de la base reguladora de la pensión por los años cotizados al 125% de la base mínima. El Estado contabiliza IRPF, cotizaciones de trabajador y empresa, imposición al consumo (10% efectivo sobre el 85% de la renta disponible — el canal de demanda de Falk-Tsoukalas en su dimensión fiscal), prestaciones pagadas, recaudación pigouviana neta de administración y tributación de la regalía.

Los perfiles se asignan así: P1 (60.000 €, casado con cónyuge sin rentas, 2 hijos, 2,1 unidades de consumo OCDE) como ingeniero senior en tramo P90–P95 OAXI con θ = 0,08; P2 (52.000 €, soltero con un ascendiente a cargo, 1,5 unidades) como técnico en tramo P50–P90 con θ = 0,03; P3 (77.500 €, casado con cónyuge con rentas, 2 hijos, 2,1 unidades) como analista BI/riesgo de crédito en el Top 20 OAXI con θ = 0,15. El IRPF se calibra perfil a perfil para reproducir exactamente las retenciones observadas en la calculadora.

## 2. Resultado central: la calibración §3.3 protege la renta solo en el Top 20

El primer hallazgo estructural es que, con κ = 1,5, el θ mínimo de retención de la ecuación (8) es ≈ 0,63 para los tres perfiles — entre 4 y 21 veces la calibración §3.3. La tokenización calibrada por OAXI **no evita el despido**: opera por el canal compensatorio de la ecuación (9), no por el canal protector de la ecuación (7). El trabajador es desplazado en S1, S2 y S3; lo que cambia es su tasa de recuperación de renta η.

| Perfil | η (S1, sin política) | η (S2, pigouviano) | η (S3, tokenización §3.3) | NPV trabajador S3−S2 |
|---|---|---|---|---|
| P1 (θ=0,08) | 0,52 | 0,82 | 0,70 | **−44.274 €** |
| P2 (θ=0,03) | 0,53 | 0,82 | 0,59 | **−73.477 €** |
| P3 (θ=0,15) | 0,51 | 0,79 | 0,82 | **+14.231 €** |

Sin política, el desplazamiento a los 55 destruye prácticamente la mitad de la renta neta esperada de la década (η ≈ 0,51–0,53): la prestación topada apenas repone el 40–44% del neto previo durante dos años y el subsidio posterior cae al 13–15%. El impuesto pigouviano al 20% eleva η a ≈ 0,80 de forma **uniforme**. La tokenización §3.3 produce resultados **heterogéneos**: supera al pigouviano solo para el Top 20 OAXI (P3) y queda por debajo para los tramos medios — exactamente la Limitación 3 del paper, pero invertida: con la calibración actual, es la tokenización la que infracompensa a los tramos P50–P95.

Para cerrar la brecha (η = 1, Corolario 2 de Falk-Tsoukalas) la ecuación (9) en términos brutos exige θ ≈ 0,17–0,19. Pero hay una **cuña fiscal no contemplada en el paper**: como la regalía tributa (RCM 19–28%), el θ que logra η = 1 en renta *neta* es 0,22–0,24, un 26% superior al teórico. La banda superior de la tabla §3.3 (0,20) es por tanto insuficiente incluso para el Top 20 si el objetivo es la recuperación plena neta.

## 3. Impacto en dependientes (renta equivalente por unidad de consumo)

La renta neta media anual por unidad de consumo OCDE-modificada cae así respecto a continuidad:

| Perfil (hogar) | S0 | S1 | S2 | S3 §3.3 |
|---|---|---|---|---|
| P1 — pareja + 2 hijos (2,1 u.c.) | 20.341 € | 10.651 € (−48%) | 16.728 € (−18%) | 14.257 € (−30%) |
| P2 — soltero + ascendiente a cargo (1,5 u.c.) | 25.303 € | 13.286 € (−47%) | 20.684 € (−18%) | 14.942 € (−41%) |
| P3 — pareja + 2 hijos (2,1 u.c.) | 26.234 € | 13.262 € (−49%) | 20.658 € (−21%) | 21.453 € (−18%) |

Dos observaciones. Primera, el hogar de P1 (cónyuge sin rentas, dos hijos) cae sin política por debajo del umbral de riesgo de pobreza relativa para su tipo de hogar pese a partir de un salario de 60.000 €: el tope de la prestación convierte la progresividad del sistema de protección en regresividad efectiva para salarios medios-altos. Segunda, el caso más vulnerable bajo tokenización es P2: la combinación de θ bajo (0,03) y un dependiente mayor a cargo produce la mayor caída relativa de los escenarios con política (−41%), señalando que cualquier despliegue real necesitaría un suelo de θ o la compatibilidad con el canal fiscal para los tramos medios.

## 4. Pensiones: la segunda ola del coste

El desplazamiento a los 55 erosiona la base reguladora ≈ 19–21% (dos años de prestación cotizando por base previa, ocho de subsidio cotizando al 125% de la base mínima). En términos de NPV a la fecha de jubilación, la pérdida de pensión vitalicia asciende a 88.000–96.000 € adicionales por trabajador — un coste que recae sobre el trabajador pero también reduce la futura presión sobre el sistema de pensiones de forma perversa: vía menores derechos, no vía menores necesidades. Ni el pigouviano (transferencia no cotizable) ni la regalía (RCM, no cotizable) reparan este canal: **ambos mecanismos dejan intacta la brecha de cotización**, lo que sugiere como extensión natural del diseño tokenizado la posibilidad de destinar una fracción del depósito subyacente (§3.1.bis del paper) a convenio especial con la Seguridad Social.

## 5. Cuentas del Estado: coste fiscal, presión y esfuerzo

Frente a la continuidad (S0), el coste fiscal por trabajador desplazado (NPV 10 años: recaudación perdida de IRPF + cotizaciones + IVA, más prestaciones pagadas, menos nuevos ingresos) y su agregación a la población objetivo española del paper (~165.000 trabajadores, 0,75% de la ocupación) es:

| Escenario | Coste fiscal NPV/trabajador | Coste agregado (anualidad) | % PIB anual | Δ presión fiscal | Δ esfuerzo fiscal |
|---|---|---|---|---|---|
| S1 sin política | 249.389 € | 4.824 M€/año | 0,292% | +0,29 p.p. | +0,78% |
| S2 pigouviano | 213.788 € | 4.135 M€/año | 0,251% | +0,25 p.p. | +0,67% |
| S3 tokenización | 223.284 € | 4.319 M€/año | 0,262% | +0,26 p.p. | +0,70% |

La lectura estratégica es triple. Primera: el grueso del coste fiscal (≈ 85%) no son las prestaciones sino la **recaudación evaporada** — IRPF, cotizaciones y consumo del salario destruido. Por eso ninguno de los dos mecanismos lo neutraliza: el pigouviano recupera para el Estado el 10% retenido de τ más el IRPF de la transferencia; la tokenización aporta solo el RCM de la regalía (19–28% de un flujo menor). Segunda: si el Estado quisiera cubrir el coste del escenario sin política con impuestos generales, necesitaría elevar la presión fiscal ~0,29 p.p. de PIB, lo que sobre una presión del 37,5% supone un incremento del esfuerzo fiscal del 0,78% para el conjunto de la sociedad — y esto solo para el 0,75% de la ocupación; una segunda ola que alcanzara al cuartil Q1 completo del OAXI multiplicaría la cifra por un orden de magnitud. Tercera: la diferencia entre mecanismos para el Estado (≈ 184 M€/año a favor del pigouviano en el caso base) es pequeña frente a la diferencia entre *tener* mecanismo y no tenerlo (≈ 500–690 M€/año), y se invierte cuando θ se calibra al alza: con θ = θ_η1 la tokenización genera más RCM e IVA y el coste fiscal cae por debajo del pigouviano.

En bienestar agregado (suma Kaldor-Hicks de trabajador + firma + Estado), los tres escenarios con automatización superan a la continuidad (la automatización crea excedente cuando V > wᴵ: el problema es distributivo, coherente con la tesis del paper), y S2 y S3 están prácticamente empatados (diferencia < 0,6% del total): la dominancia de la Proposición 1 **no se decide en el agregado sino en la calibración distributiva y en quién soporta el coste del mecanismo**.

## 6. Variables críticas a nivel estratégico

El análisis de sensibilidad (tornado sobre el diferencial NPV S3−S2, rangos: κ ∈ [1; 3], τ ∈ [0,1; 0,3], θ por tramos §3.3, c_tax ∈ [0,05; 0,15], hazard ∈ [0,05; 0,25], penalización ∈ [0,15; 0,40], r ∈ [0,02; 0,05]) identifica jerarquías distintas por actor.

**Para el profesional**, las variables críticas son, por este orden: (1) **τ y κ_V** (amplitudes de ±110.000 € y ±102.000 € en el NPV a 10 años) — la elección entre mecanismos le importa menos que la generosidad del que se adopte; (2) **θ de su tramo** (±54.000 €): para P1 y P2 la diferencia entre el suelo y el techo de su banda §3.3 vale más que cualquier otra decisión a su alcance, lo que convierte la negociación colectiva del λ sectorial en su margen estratégico principal; (3) el **tratamiento fiscal de la regalía** y, sobre todo, la **cuña fiscal del 26%** sobre el θ requerido; (4) el hazard de reempleo y la penalización salarial no discriminan entre mecanismos pero determinan el tamaño absoluto de la pérdida — su variable defensiva real es la empleabilidad, que ningún mecanismo sustituye; y (5) la brecha de cotización de pensiones (~90.000 € NPV), invisible en la discusión corriente.

**Para la empresa**, las variables críticas son: (1) **τ vs. θ·κ** — la firma es indiferente entre mecanismos cuando θ·κ = τ, es decir, cuando la regalía iguala al impuesto como fracción del coste laboral; con la calibración base, la firma con plantilla P1/P2 *prefiere la tokenización* (θV < τw) y la firma con plantilla Top 20 *prefiere el pigouviano* (0,225w > 0,2w) — un mapa de adopción voluntaria inverso al deseable, que confirma la necesidad del mínimo mandatorio de §5.2; (2) **κ_V**, que es simultáneamente su incentivo a automatizar y la base de la regalía: la firma tiene incentivo a infradeclarar V, lo que hace de la **auditabilidad del flujo del activo agéntico** la variable de diseño institucional decisiva (metadatos, Shapley — §5.1); (3) la condición de devengo sobre ingresos (canal Weitzman, no simulado aquí), que convierte θV en coste variable frente al pigouviano fijo — ventaja en recesión; y (4) F+K: con indemnizaciones españolas (33 días/año, 20 años de antigüedad) el término (F+K)·r apenas representa el 5% de wᴵ — la protección por costes de despido es ya hoy irrelevante frente a la sustitución agéntica, validando empíricamente la disolución §2.4.bis en el caso español.

**Para el Estado**, las variables críticas son: (1) la **recaudación evaporada** como componente dominante del coste — la política óptima fiscal es la que maximiza la masa salarial gravable retenida, lo que favorecería θ altos (cercanos a θ_min de retención) sobre cualquier esquema compensatorio; (2) **c_tax vs. c_token** (±11.000 € por trabajador): la ventaja administrativa de la tokenización (canal privado, 1% vs. 10%) es real pero de segundo orden; (3) el **tratamiento RCM vs. trabajo de la regalía**: gravarla como trabajo recauda más pero eleva el θ requerido para η = 1 de 0,22 a ~0,28, trasladando el coste a la firma — un trade-off de incidencia puro; (4) la **escala de la población expuesta**: el salto de 0,29 p.p. de presión fiscal es absorbible para el 0,75% de la ocupación, pero el esfuerzo fiscal crece de forma no lineal si la frontera agéntica avanza al Q1 completo (~10% de la ocupación), donde hablaríamos de ~3 p.p. de PIB — el orden de magnitud de la recaudación total del Impuesto de Sociedades; y (5) la interacción con pensiones, donde ambos mecanismos generan un pasivo contingente diferido que no aflora en el horizonte presupuestario corriente.

## 7. Implicaciones para el Paper 8B

Cuatro resultados de la simulación son directamente incorporables al texto. Primero, la calibración §3.3 y la condición de retención (8) son cuantitativamente incompatibles en el caso español salvo κ muy altos: convendría explicitar que la tabla §3.3 calibra el canal η (ec. 9) y no el canal protector (ec. 7), y que la retención exige θ ≈ 0,3–0,6 — solo alcanzable en el modelo de bolsa colectiva tipo MBB. Segundo, la cuña fiscal sobre la regalía (+26% sobre el θ teórico para η = 1 neto) debería incorporarse a la ecuación (9) como η_j(θ_j) = η₀ + (1−t_RCM)·θ_j·V_j/wᴵ_j. Tercero, el mapa de incentivos de adopción voluntaria por composición de plantilla (la firma intensiva en Top 20 prefiere el impuesto) refuerza el argumento del mínimo mandatorio de §5.2 con una microfundamentación nueva. Cuarto, la dominancia en bienestar agregado entre mecanismos es empíricamente estrecha en horizonte finito; la dominancia robusta de la tokenización aparece en tres dimensiones que el agregado no captura: heterogeneidad distributiva (cuando θ se calibra bien), independencia del ciclo político, y el canal de pensiones/Weitzman si el depósito subyacente se conecta a cotización.

## Anexo: parámetros del caso base

Horizonte 10 años; r = 3% real; κ_V = 1,5; τ = 20% (N = 10); c_tax = 10%; c_token = 1%; cotización empresarial 31% sobre base topada en 60.000 €/año; hazard de reempleo 15% anual; penalización salarial 28%; IPREM 600 €/mes; tope prestación 1.225/1.575 €/mes (0/2 hijos); IVA efectivo 10% sobre MPC 85%; F = 33 días/año × 20 años; K = 0,5 × bruto; regalía gravada como RCM; base reguladora a 25 años. Archivos: `modelo.py` (motor), `analisis.py` (sensibilidad y figuras), `resultados_base.csv`, `thetas.csv`, `pensiones.csv`, `agregado_estado.csv`, `tornado.csv`, figuras 1–3.

---

## Addendum (recálculo): pigouviano con afectación íntegra e ineficiencia del 20% / 35% / 45%

Se recalcula S2 bajo dos cambios: la recaudación se afecta íntegramente a compensar la caída salarial (el Estado no retiene margen) y el canal fiscal soporta una pérdida de ineficiencia —peso muerto— del 20%, 35% o 45% del flujo. La tokenización mantiene c_token = 1% y θ §3.3.

| Ineficiencia | η S2 (media) | Coste fiscal agregado S2 | Bienestar S3−S2 (€/trab., media) | Preferencia del trabajador |
|---|---|---|---|---|
| 20% | 0,78 | 4.453 M€/año (0,270% PIB) | +24.755 | P3 → S3; P1, P2 → S2 |
| 35% | 0,73 | 4.525 M€/año (0,274% PIB) | +47.043 | P3 → S3; P1, P2 → S2 |
| 45% | 0,70 | 4.571 M€/año (0,277% PIB) | +61.914 | P3 → S3; P1 ≈ indiferente; P2 → S2 |

S3 (tokenización): coste fiscal constante 4.319 M€/año (0,262% PIB).

Con ineficiencia realista, la jerarquía se invierte en dos de los tres planos. En **bienestar agregado**, la tokenización pasa a dominar Kaldor-Hicks en los tres tramos y en los tres perfiles (de +17.630 a +77.469 € por trabajador): el peso muerto del canal fiscal destruye excedente que el canal contractual privado no destruye, y la ventaja crece monótonamente con la ineficiencia. En **coste para el Estado**, la afectación íntegra elimina el margen retenido y S2 pasa a costar más que S3 en todos los tramos (la tokenización conserva el RCM de la regalía y más IVA). En el plano **individual**, sin embargo, la calibración §3.3 sigue sin alcanzar: el break-even de ineficiencia al que el trabajador es indiferente entre mecanismos es del 46,8% para P1 (θ=0,08), del 79,9% para P2 (θ=0,03) y ≈0% para P3 (θ=0,15). Es decir: incluso con un canal fiscal que pierde un tercio por el camino, el trabajador de tramo medio sigue prefiriendo el impuesto, porque un 65% de τ·wᴵ = 0,13·wᴵ supera a θ·V = 0,045–0,12·wᴵ. La conclusión principal se refina, no se altera: la ineficiencia pigouviana restituye la Proposición 1 en el agregado para todo el rango 20–45%, pero la dominancia *individual* y por tanto la viabilidad política del mecanismo siguen dependiendo de elevar θ hacia θ_η1 neto (0,22–0,24). Archivos: `recalculo_ineficiencia.csv`, `fig4_ineficiencia.png`.

---

## Addendum 2 (recálculo): sistema de royalties acumulativo con wallet custodiada

Se sustituye la regalía plana por un sistema acumulativo: cada año trabajado genera derechos sobre la cosecha (*vintage*) de proyectos de ese año, cuyo flujo decae al 15% anual (decaimiento geométrico cuya vida media es ≈ 6,7 años, consistente con la vida media de proyecto de 6 años). Los derechos se abonan como tokens a una wallet personal custodiada por la empresa con rendimiento del 0,5–1,9% anual (base 1,2%), tributando como RCM en el devengo. La acumulación cubre 20 años de carrera (edad 35→55); el valor de cada vintage se normaliza a v = 0,15·V de modo que el flujo estacionario en empleo converge a θ·V (mismo flujo que el sistema plano: la comparación aísla el efecto de la arquitectura acumulativa, no de la generosidad).

| Perfil | η acumulativo | Wallet a los 55 | NPV trab. vs pigou (i=20%/35%/45%) | Coste fiscal vs S2 |
|---|---|---|---|---|
| P1 (θ=0,08) | 0,90 | 119.376 € | **+39.850 / +58.027 / +70.162 €** | −1.507 a −7.295 € |
| P2 (θ=0,03) | 0,66 | 39.002 € | −39.447 / −23.671 / −13.153 € | +9.488 a +4.493 € |
| P3 (θ=0,15) | 1,16 | 270.883 € | **+192.676 / +214.317 / +229.145 €** | −22.980 a −30.598 € |

Tres resultados cambian la geometría del problema. Primero, **la arquitectura acumulativa desplaza el umbral de dominancia individual hacia abajo**: P1 (tramo P90–P95), que con la regalía plana necesitaba una ineficiencia pigouviana del 46,8% para preferir la tokenización, ahora la prefiere en los tres tramos (η = 0,90 vs. 0,71–0,79). La razón es la **prefinanciación**: la wallet convierte 20 años de expropiación silenciosa en un colchón de autoseguro (119.000–271.000 €) disponible en el momento exacto del desplazamiento, mientras el pigouviano solo existe tras el despido. Segundo, **P3 cruza η > 1** (1,16): el Top 20 entra en el territorio del Corolario 2 invertido de Falk-Tsoukalas (η > 1 ⇒ subautomatización), lo que sugiere que con arquitectura acumulativa el techo θ = 0,20 de la tabla §3.3 es ya *excesivo* para el Top 20 — la calibración óptima de θ baja cuando el sistema acumula. Tercero, **P2 sigue sin cruzar** (η = 0,66): con θ = 0,03 ni la acumulación basta; el suelo de la tabla para P50–P90 es la pieza inequívocamente infracalibrada del diseño.

Advertencia metodológica de contabilidad inter-temporal: la anualidad de la wallet que el trabajador consume en 55–65 fue financiada por la firma durante 35–55, fuera de la ventana de comparación. El sistema acumulativo no crea ese valor gratis: lo *difiere y lo asegura*. Su superioridad no es de coste total sino de **sincronización** — paga durante la cristalización (cuando el paper sitúa la expropiación, §2.4: «expropiado pero retenido») y entrega la liquidez en el momento del shock. El rendimiento de la wallet es de segundo orden (la banda 0,5–1,9% mueve el NPV del trabajador menos del 3%); las variables críticas del sistema acumulativo son la duración de la carrera acumulada, el decaimiento del 15% (que gobierna cuánto «sobrevive» del stock de derechos al despido: el 96% del flujo estacionario a los 20 años de carrera, decayendo a la mitad cada 4,3 años después) y, como siempre, θ. Para el Estado, el acumulativo es más barato que el pigouviano en P1 y P3 (recauda RCM durante 20 años antes del despido y sobre el rendimiento de la wallet) y para la firma constituye financiación cautiva a 1,2% frente al 3% de mercado (§3.1.bis). Archivos: `acumulativo.py`, `resultados_acumulativo.csv`, `fig5_evolucion_temporal.png`.
