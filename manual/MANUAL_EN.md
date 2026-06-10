# Methodological Manual — v1.0

**Pigouvian Tax vs Royalties Token** · Comparative simulator of compensation mechanisms for agentic-AI displacement
Framework: ITEA · Paper 8B "The Tokenized Residual Right" (A. García-Lluis Valencia, 2026)

---

## 1. Purpose

This project quantitatively compares two responses to labour displacement by agentic AI: the **Pigouvian automation tax** (Falk-Tsoukalas) and the **tokenized residual right** — a royalty for the transfer of the worker's intellectual capital (IC) into the firm's algorithmic asset, calibrated by occupational exposure (ITEA/OAXI). The simulator evaluates both systems for four stakeholders (worker, firm, State, taxpayer) across nine countries, over a 35-to-65 life cycle.

## 2. Theoretical framework

The Pigouvian tax corrects a **demand externality**: the automating firm captures 100% of the cost saving but suffers only 1/N of the damage that wage destruction inflicts on aggregate demand; the optimal rate is τ\* = f·(1−1/N). The residual right starts from the **algorithmic expropriation** diagnosis (Paper 8B): the crystallisation of the worker's tacit knowledge (Polanyi; Nonaka-SECI) into the firm's algorithmic assets is an unremunerated capital transfer that the industrial labour contract does not contemplate (Williamson; Hodgson). The royalty θ·V is the consideration for that transfer; its two formal channels are the retention condition (eq. 8) and the income recovery rate η (eq. 9).

## 3. Simulator architecture

Flow: **country → occupation (O*NET Title, ITEA percentile) → gross salary (pop-up) → Pigouvian module ‖ royalty module → verdict per stakeholder + time progression + generated interpretation**. All numeric parameters are continuous sliders within their range; "default" values are only the initial position. Real terms throughout (3% discount).

## 4. Country salary module

Each country is parameterised with: bracketed income-tax schedule, employee social contributions (rate and cap), **employer contributions** (defining total labour cost wᴵ = gross + employer SSC — the tax base and the reference for V), savings/capital taxation (taxes the royalty), effective consumption taxation (fiscal demand channel), unemployment benefit cap and assistance level, and taxpayer population. Validation sources: the selected per-country calculators (Cinco Días ES; code.travail.gouv.fr FR — the only official one with employer cost; Sparkasse DE; CalcolaStipendioNetto/Stipendee IT; SD Worx BE; Doutor Finanças/Literacia PT; The Salary Calculator/MoneyHelper UK; ADP/SmartAsset US; Wealthsimple CA), anchored for comparability on **OECD Taxing Wages**.

## 5. Pigouvian module — foundation of each variable

| Variable | Range (default) | Foundation |
|---|---|---|
| τ — rate on saved labour cost | 0.5–50% (20%) | Free slider with the 10–30% literature zone marked. Within 0.5–50% the tax is redistributive, not preventive: the firm still saves ≥50% of labour cost. |
| N — competitive structure | 2–60 (sectoral) | Effective N = 1/HHI, calibrated with Forbes Global 2000 sales shares by industry. Sets the share of demand damage the firm ignores: (1−1/N). |
| f — externality intensity | 0.10–0.40 (derived) | f ≈ (MPC_workers − MPC_capital) × multiplier × pass-through ≈ 0.2–0.3. In free mode the implied f = τ/(1−1/N) is displayed as a consistency check. |
| i — fiscal channel inefficiency | 5–45% (20%) | Floor: administrative cost of active programmes (Card-Kluve-Weber, 5–15%). The 20/35/45% tranches: marginal cost of public funds (Ballard et al.; Feldstein). |
| α — revenue earmarking | 0–100% (100%) | α=1: fully earmarked compensation. α<1 models budget capture; the tax becomes a revenue source exactly insofar as it stops compensating. |
| D — transfer duration | 1–10 yrs (10) | From mirroring the benefit (2) to a bridge income until retirement. |
| t_tr — transfer taxation | 0–45% (15%) | From exempt (severance-style) to full labour income. |
| λ_t — take-up | 70–100% | Documented non-take-up of conditional programmes (15–30%). |
| e — base erosion | 0–30% | Definitional avoidance ("what counts as a robot/agent?"), the standard robot-tax critique (Abbott-Bogenschneider). |

## 6. Royalty module — foundation of each variable

| Variable | Range (default) | Foundation |
|---|---|---|
| θ — residual right, P50–P95 bracket | 0.25–15% (5%) | ITEA brackets merged by v1.0 design decision; log scale recommended. Marked red below the participation condition. |
| θ — Top 20 OAXI | 5–20% (12.5%) | Overcompensation flag if η>1 (under-automation, inverted Corollary 2). |
| κ_V — asset multiplier | 1.0–4.0 (sectoral) | V = κ·wᴵ. Calibrated: κ ≈ 1 + profit_per_employee/wᴵ from Forbes 2024 medians (retail 1.3 … banking 2.2); ceiling = sales/employee÷wᴵ as a bargaining bound. |
| Architecture | flat / **cumulative** | The cumulative version accrues rights by annual *vintages*: it pays when the IC transfer happens, not when the dismissal does. v1.0 result: it lowers the dominance θ\* and makes it decreasing in age. |
| δ — vintage decay | 10–25% (15%) | Annual value loss of each project's harvest. δ=15% ⇒ geometric mean life ≈ 6.7 years, consistent with a 6-year project life. Sectoral proxy: Δ capital intensity in the 2014–2024 Forbes panel. |
| Accumulated career years | 5–35 (20) | Ramp 1−(1−δ)^s towards the steady flow θ·V (96% at 20 years). Below ~7 years the cumulative pays less than the flat. |
| Wallet: CPI deposit | 0–100% (50%) | Custodied tokens indexed to inflation: 0% real, no market risk, counterparty risk remains. |
| Wallet: internal financing | complement | The balance lends to company projects as an internal financial product (Pensionsrückstellungen/Genussschein channel, paper §3.1.bis). |
| Financing spread | CPI+0.5 – CPI+4% (2%) | Bounded between the deposit and the firm's real cost of debt (~3%): the distribution key of the financial surplus. Concentration warning if internal allocation exceeds 50% (Enron-401k risk). |
| Annual withdrawal | 0–100% (0%) | In-career cash-out; erodes self-insurance. Taxation can disincentivise without prohibiting. |
| Royalty taxation | country capital tax | Taxed as savings income on accrual. Key wedge: it raises the full-recovery θ ~26% above the gross theoretical value. |
| Insolvency guarantee | FOGASA-type fund / segregation | A design condition, not an option: the insured event correlates with insolvency. |

## 7. Firm calibration (Forbes Global 2000)

Source: the 2014 list (original xls), 2019 and 2024 (panel; the 2024 sheet includes **employees and industry**: 1,943 valid firms). Products: median sales and profit per employee by harmonised sector (24 sectors), margins, HHI and effective N per industry, and the 2014→2024 capital-deepening panel (an automation-speed proxy). Limitations: current dollars, universe truncated to large listed firms (κ is an upper bound for SMEs), EBITDA unavailable (complement with Damodaran margins).

## 8. Displacement and pensions engine

Dismissal at the configured age; cycle: capped contributory benefit for 24 months (per country) → assistance → re-employment with an annual hazard (15% for seniors) and wage penalty (28%). Pension memo (ES case): ≈20% erosion of the pension base (≈ €90,000 lifetime NPV) that **neither** mechanism repairs — motivating the option of allocating part of the deposit to pension contributions.

## 9. Derived outputs (always visible)

Retention θ_min (eq. 8): (wᴵ−(F+K)·r)/V. Full-recovery θ_η1, gross and **net** of the fiscal wedge. **Participation condition**: θ ≥ τ·wᴵ·(1−i)·α/V — the floor that makes the royalty preferred to the prevailing tax. Implied f. η>1 flag.

## 10. Key v1.0 results

(1) The worker's θ\* frontier is narrow: 1.5–7.7% over the entire plausible space; with θ≥5% the cumulative royalty dominates in all nine countries. (2) **Age reverses the ranking**: θ\* falls from ~8.5% (dismissal at 45) to ~1.6% (at 60) under the cumulative architecture, and rises under the flat one ⇒ the systems complement each other across cohorts; the hybrid optimum crosses at ages 48–52. (3) Three country blocs: continental (high wedge: a powerful but expensive tax), Anglo (η₀=0.46: the royalty wins earlier and where it is most needed), low-wage (high η₀: both add less). (4) For the State and the taxpayer the royalty costs 26–39% less under full earmarking. (5) For the firm the royalty is **more expensive in present value** (it pays earlier), but a **contracting zone** θ∈[3.7%, 5.0%] exists at τ=20% where both parties prefer it — the tax is the credible threat that opens it; internal financing recovers ~16% of the cost.

## 11. v1.0 limitations

Approximate parametric national taxation (fine validation pending against the selected calculators); simplified unemployment; illustrative ITEA percentiles in the selector (replace with the ITEA v3.0 series); the Weitzman channel (revenue-contingent accrual over the cycle) not simulated; no general equilibrium (exogenous prices and wages); life-cycle comparison with the timing caveat (the firm pre-funds the wallet).

## 12. Reproducibility

`src/modelo.py` (ES base engine) → `src/acumulativo.py` (vintages+wallet) → `src/fronteras.py` (9 countries, θ\* grids) → `src/calibracion_forbes.py` (κ, HHI, panel) → `src/figs_pdf.py` + `src/informe_pdf.py` (ES/EN PDF reports). Data in `data/`, figures in `figures/`, dashboard in `docs/index.html` (GitHub Pages).
