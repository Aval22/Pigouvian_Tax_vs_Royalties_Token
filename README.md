# Pigouvian Tax vs Royalties Token

**🇪🇸** Simulador comparado: impuesto pigouviano a la automatización vs. royalties tokenizados por transferencia de capital intelectual (Marco ITEA · Paper 8B). **🇬🇧** Comparative simulator: Pigouvian automation tax vs. tokenized intellectual-capital royalties (ITEA Framework · Paper 8B).

**🔗 Dashboard (GitHub Pages):** https://aval22.github.io/Pigouvian_TAX_vs_Royalties_token/

| | |
|---|---|
| 📘 Manual metodológico / Methodological manual | [`manual/MANUAL_ES.md`](manual/MANUAL_ES.md) · [`manual/MANUAL_EN.md`](manual/MANUAL_EN.md) |
| 📄 Informes / Reports (PDF) | [`reports/Informe_ITEA_ES.pdf`](reports/Informe_ITEA_ES.pdf) · [`reports/Informe_ITEA_EN.pdf`](reports/Informe_ITEA_EN.pdf) |
| 🧮 Motor de simulación / Engine | [`src/`](src/) (Python 3.12: modelo, acumulativo, fronteras, calibración Forbes) |
| 📊 Datos / Data | [`data/`](data/) (rejillas θ\*, estructura país, calibración Forbes G2000) |
| 🖥️ Dashboard estático / Static dashboard | [`docs/index.html`](docs/index.html) (React + Recharts vía CDN, ES/EN) |

## Resultados clave / Key findings (v1.0)

1. **Frontera estrecha / Narrow frontier** — θ\* del trabajador entre 1,5% y 7,7% en 9 países; con θ≥5% el royalty acumulativo domina. / Worker θ\* between 1.5–7.7% across 9 countries; with θ≥5% the cumulative royalty dominates.
2. **La edad invierte el ranking / Age reverses the ranking** — sistemas complementarios por cohortes; híbrido óptimo con cruce en 48–52 años. / Complementary systems across cohorts; hybrid optimum crossing at ages 48–52.
3. **Zona de contratación / Contracting zone** — θ∈[3,7%, 5,0%] a τ=20%: el impuesto es la amenaza creíble que hace negociable el royalty. / The tax is the credible threat that makes the royalty negotiable.
4. **Estado y contribuyente / State & taxpayer** — el royalty cuesta un 26–39% menos con afectación íntegra. / The royalty costs 26–39% less under full earmarking.

## Reproducir / Reproduce

```bash
pip install -r requirements.txt
python src/fronteras.py        # rejillas θ* (9 países, edades, arquitecturas)
python src/calibracion_forbes.py  # requiere los xlsx de Forbes en data/raw/
python src/figs_pdf.py && python src/informe_pdf.py  # informes PDF ES/EN
```

## Cita / Citation

García-Lluis Valencia, A. (2026). *Pigouvian Tax vs Royalties Token: a comparative simulator (v1.0)*. ITEA Framework. Véase / see `CITATION.cff`.

## Licencia / License

**Licencia propietaria — uso no comercial con reserva de derechos.** Propiedad intelectual de Alberto García-Lluis Valencia. Se permite el uso académico, docente y de investigación con atribución; **todo uso comercial requiere autorización escrita del autor**. El uso comercial no autorizado conlleva una indemnización del 40% de la facturación obtenida (daño emergente y lucro cesante). Véase el archivo [`LICENSE`](LICENSE).

**Proprietary license — non-commercial use with reserved rights.** Intellectual property of Alberto García-Lluis Valencia. Academic, teaching and research use permitted with attribution; **any commercial use requires the author's written authorization**. Unauthorized commercial use carries a 40% revenue indemnification (consequential damage and loss of profit). See [`LICENSE`](LICENSE).
