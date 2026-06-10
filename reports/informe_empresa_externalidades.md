# Escenarios de optimalidad, costes empresariales y externalidades: impuesto pigouviano vs. royalties por transferencia de CI

**Método:** motor del Simulador ITEA, perfil de referencia España P94 (bruto 62.000 €, wᴵ = 80.600 €, κ = 1,8 → V = 145.100 €), carrera 35→55, ventana post-despido 55→65, términos reales, k_d (coste de deuda real de la firma) = 3%. Complementa el informe de fronteras por país y edad. Archivos: `frontera_firma.csv`, `fig9_empresa.png`. · Junio 2026

---

## 1. Síntesis: en qué escenarios es óptimo cada sistema

Reuniendo las fronteras de los cuatro actores calculadas en los dos barridos, el mapa de optimalidad queda así.

**El impuesto pigouviano es óptimo cuando**: el derecho residual está calibrado bajo (θ < 2–4%, la zona inferior del tramo P50–P95); el desplazado es joven o de baja antigüedad (< 12 años de CI acumulado: sin vintages que monetizar, su problema es de transición); la arquitectura disponible es plana y no acumulativa; la ocupación está bajo el percentil 50 ITEA (fuera del ámbito de θ — el impuesto es el único instrumento universal); el país combina cuña fiscal alta con fiscalidad del capital alta (Bélgica, Francia: base imponible patronal máxima, royalty fiscalmente castigado); y el canal fiscal es excepcionalmente eficiente (i ≤ 20%) con afectación íntegra creíble. Para la **empresa**, además, el impuesto es siempre preferible cuando θ supera su frontera de aceptación (sección 3) — un matiz decisivo, porque la firma no compara flujos anuales sino valores presentes, y el calendario juega a favor del impuesto.

**El pago de royalties es óptimo cuando**: θ ≥ 4–5% (cualquier calibración de tramo medio-alto); la arquitectura es acumulativa con ≥ 15 años de carrera; el desplazado es senior (≥ 50–55 años — exactamente la población de mayor daño); el país tiene protección pública débil y fiscalidad del capital moderada (EE. UU., Reino Unido, Canadá, y España en el flanco del capital al 21%); y siempre desde la perspectiva del Estado y del contribuyente, donde domina sin excepción con afectación íntegra (coste fiscal un 26–39% menor en los nueve países). La región donde **todos** los actores pueden preferirlo simultáneamente existe, pero es estrecha: es la zona de contratación de la sección 3.

## 2. Los costes de la empresa: misma magnitud anual, calendario opuesto

La comparación de costes empresariales tiene una asimetría que los flujos anuales esconden y el valor presente revela:

| Concepto (por trabajador, perfil ES P94) | Impuesto (τ = 20%) | Royalty acumulativo (θ = 10%) |
|---|---|---|
| Coste anual estacionario | 16.244 €/año | 14.620 €/año (devengo) |
| Calendario del pago | Solo tras automatizar: años 21–30 | Desde el año 1 (rampa) hasta el 30 (decaimiento) |
| NPV del coste bruto (35–65) | **76.720 €** | 181.307 € |
| Beneficio de financiación interna | — | −28.626 € |
| **NPV del coste neto** | **76.720 €** | **152.681 €** |

A flujos anuales parecidos (el royalty del 10% cuesta incluso algo menos por año que el impuesto del 20%), el NPV del royalty **duplica** al del impuesto. La razón es puro calendario: el impuesto se paga tarde (solo cuando la automatización ocurre, a partir del año 21) y el royalty se devenga desde el primer año de transferencia de CI. Es la imagen especular exacta del resultado del trabajador: la misma sincronización temprana que convierte el royalty en seguro prefinanciado para el empleado lo convierte en pasivo anticipado para el empleador. **No hay almuerzo gratis intertemporal: la superioridad del royalty para trabajador y Estado la financia la empresa adelantando el pago.** Cualquier defensa del mecanismo debe partir de reconocer esto, y por eso los dos amortiguadores de la sección siguiente —la financiación interna y la amenaza fiscal— no son accesorios sino constitutivos del diseño.

## 3. La frontera de la empresa y la zona de contratación

Resolviendo el θ máximo que la firma acepta antes de preferir el impuesto (NPV neto royalty = NPV impuesto):

| θ máximo aceptable para la firma | spread IPC+0,5% | IPC+2,0% | IPC+3,5% |
|---|---|---|---|
| τ = 10% | 2,7% | 2,5% | 2,4% |
| τ = 20% | 5,3% | 5,0% | 4,7% |
| τ = 30% | 8,0% | 7,5% | 7,1% |
| τ = 40% | 10,7% | 10,0% | 9,4% |

Cruzando esta frontera con la del trabajador (informe anterior: θ\* = 3,5–4,1% a τ=20%, i=35%) aparece el resultado central de este informe: **existe una zona de contratación** — un intervalo de θ donde trabajador y empresa prefieren *ambos* el royalty al impuesto. A τ = 20%: **θ ∈ [3,7%, 5,0%]**. A τ = 30%: θ ∈ [5,5%, 7,5%]. A τ = 10% la zona casi desaparece (θ ∈ [2,1%, 2,5%]).

Dos lecturas de primer orden. Primera: **la zona existe gracias a la ineficiencia del canal fiscal y al beneficio de financiación** — el peso muerto que el impuesto destruye (i × τ × wᴵ) y el ahorro financiero de la wallet son el excedente que las partes se reparten al contratar el royalty en lugar de sufrir el impuesto. Segunda, y más profunda para el Paper 8B: **el ancho de la zona crece con τ**. El impuesto pigouviano no es la alternativa al royalty: es la *amenaza creíble* que lo hace negociable. Sin un impuesto en el horizonte (τ = 0), la firma nunca acepta voluntariamente θ > 0 (su frontera es cero); con τ = 30% anunciado, acepta hasta el 7,5%. La arquitectura institucional óptima no es "impuesto o royalty" sino **impuesto como opción de salida legislada + royalty negociado dentro de la zona** — exactamente la estructura de los convenios con cláusula de descuelgue, ahora microfundamentada.

## 4. El canal de financiación interna, cuantificado

La wallet custodiada convierte el pasivo de royalties en fuente de financiación a coste IPC+spread, por debajo del coste de deuda de mercado (k_d ≈ 3% real). Para una firma con 1.000 trabajadores expuestos y θ = 10%:

| Spread pactado | Pool de wallet máximo | Ahorro financiero (NPV/trabajador) | Ahorro anual en el pico |
|---|---|---|---|
| IPC + 0,5% | 171,4 M€ | 37.489 € | 4.713 €/trabajador |
| IPC + 2,0% | 181,8 M€ | 28.626 € | 3.636 €/trabajador |
| IPC + 3,5% | 193,1 M€ | 18.802 € | 2.414 €/trabajador |

El pool alcanza los 171–193 millones de euros — del orden del 1–2% del balance de una firma del Forbes 2000 mediana, y comparable a una emisión de bonos corporativos pequeña. El ahorro financiero compensa en torno al **16% del coste bruto del royalty** (28.600 de 181.300 € NPV con spread del 2%). El spread es la llave de reparto de ese excedente financiero: a IPC+0,5% la firma captura casi todo (es financiación casi gratis, pero el trabajador apenas bate la inflación); a IPC+3,5% el trabajador captura la mayor parte y el canal pierde atractivo para la firma. El punto medio (IPC+2%) reparte aproximadamente a medias y deja a ambos mejor que la alternativa exterior (la firma se financia 100 pb bajo mercado; el trabajador rinde 200 pb sobre el depósito). Es, en miniatura, el mecanismo Pensionsrückstellungen alemán que el §3.1.bis del paper invoca: las provisiones de pensiones como capital paciente interno — con la diferencia de que aquí el derecho subyacente es el CI transferido, no el salario diferido.

Escalado nacional como referencia: 165.000 trabajadores expuestos × wallet media generan un pool agregado del orden de **20.000–30.000 M€** — un segundo pilar de ahorro cuasi-previsional surgido del propio proceso de automatización, con efectos macro propios (sección 5).

## 5. Mapa de externalidades del modelo

**Externalidades que el royalty corrige y el impuesto solo compensa.** La externalidad de demanda de Falk-Tsoukalas (cada euro de salario destruido evapora ~0,55 € de consumo por la brecha de PMC) es el fundamento de ambos mecanismos, pero operan distinto: el impuesto la *compensa ex post* con pérdida de carga (el peso muerto i destruye 20–45 céntimos por euro canalizado), mientras el royalty la *previene en origen* manteniendo un flujo de renta ligado al activo que sustituyó al salario, sin intermediación fiscal (c_token ≈ 1%). La externalidad fiscal —la recaudación evaporada, el 85% del coste público del desplazamiento— la reduce más el royalty (la fiscalidad del capital grava el flujo durante toda la carrera, no solo tras el despido). Y hay una externalidad de conocimiento que solo el royalty toca: al remunerar la transferencia de CI, elimina el incentivo del trabajador a *atesorar* conocimiento tácito como autoprotección (el hold-up del modelo SECI) — la codificación deja de ser autodestructiva. El impuesto, que grava a la firma por automatizar, si acaso incentiva lo contrario: ocultar la automatizabilidad.

**Externalidades negativas que el modelo de royalties crea y debe gestionar.** Tres, por orden de gravedad. Primera, la **concentración de riesgo**: empleo, ahorro acumulado y crédito a proyectos en la misma entidad, con la agravante de que el evento asegurado (despido por automatización) correlaciona con las fases de reestructuración y, en el límite, con la insolvencia — es el problema Enron-401(k), y exige fondo de garantía tipo FOGASA o segregación patrimonial como condición de diseño, no como opción; sin ella, la externalidad acaba en el Estado como asegurador implícito. Segunda, el **riesgo de aceleración**: una vez devengados los vintages, el coste marginal de despedir cae (el stock ya está pagado), lo que puede adelantar la sustitución — mitigable con devengo continuado condicionado a permanencia, pero es una tensión real del diseño. Tercera, la **desintermediación**: el pool de 20.000–30.000 M€ que se financia dentro de las empresas es crédito que no pasa por bancos ni mercados — eficiente para las partes, pero opaco para la supervisión financiera si escala (un sistema de pasivos cuasi-financieros fuera de balance regulatorio), lo que pide un régimen de transparencia análogo al de los planes de empleo.

**Externalidades del impuesto que el royalty evita.** El peso muerto del canal fiscal (la mayor, ya cuantificada); la elusión definicional (reclasificar qué cuenta como "agente" erosiona la base — el problema clásico del robot tax, sin equivalente en el royalty, cuyo hecho generador es la transferencia de CI observable en el propio despliegue del activo); la traslación a precios (en sectores concentrados, parte de τ acaba en el consumidor — la incidencia del royalty recae en cambio sobre el excedente del activo); y el riesgo de ciclo político (la transferencia depende de presupuestos anuales; el royalty es contractual y sobrevive a los gobiernos).

## 6. Conclusión operativa

El sistema de royalties no es más barato que el impuesto para la empresa — es más caro en valor presente (152.700 vs 76.700 € netos por trabajador en el caso central) porque paga antes, que es precisamente su virtud para todos los demás actores. Lo que lo hace contratable son tres piezas que este informe cuantifica: la financiación interna recupera ~16% del coste (y crea un pool de capital paciente de escala macro), la ineficiencia del canal fiscal genera el excedente a repartir, y la amenaza creíble de un τ alto abre la zona de contratación θ ∈ [3,7%, 5,0%] (a τ=20%) donde trabajador y empresa prefieren ambos el contrato al impuesto. La recomendación de diseño que se deriva: legislar el impuesto como régimen subsidiario con τ ≥ 20%, y permitir el descuelgue hacia royalties acumulativos negociados dentro de la zona, con garantía de insolvencia obligatoria y spread de financiación interna como variable de reparto en convenio.

*Advertencias: perfil único de referencia (P94/κ=1,8; con κ de banca 2,2 las fronteras de la firma se relajan ~20%); k_d = 3% real uniforme (firmas con peor acceso a crédito valoran más el canal de financiación y aceptan θ mayores); el coste del royalty está computado a devengo pleno — con vesting o cláusulas de permanencia el NPV empresarial baja; fiscalidad aproximada 2026.*
