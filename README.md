# EU Funding Intermediary Analysis

> A full-cycle research and analysis project built to help companies identify, evaluate, and approach European Investment Fund (EIF)-backed financial intermediaries for project funding.

**Data source:** [European Commission — Access to EU Finance Portal](https://youreurope.europa.eu/business/finance-funding/getting-funding/access-finance/en/financial-intermediaries)
**Data collected:** March 2025

---

## The Problem This Solves

Most companies — especially those in clean energy, water, and sustainability — are unaware of the structured EU funding ecosystem available to them. The European Commission's portal lists hundreds of financial intermediaries, but with no guidance on which ones fit a specific company's profile, location, or project type.

This project bridges that gap by:
1. Curating and cleaning the raw intermediary data
2. Building a decision framework to match companies to the right funds
3. Analyzing and scoring fund managers by project fit
4. Delivering analysis reports for executive and operational audiences

---

## Repository Structure

```
eu-funding-intelligence/
│
├── README.md                            ← You are here
├── INSIGHTS.md                          ← Key findings from the analysis
│
├── 01_data/
│   ├── raw/                             ← Original source data from EU portal
│   └── processed/                       ← Cleaned, structured CSV ready for analysis
│
├── 02_python_analysis/
│   ├── 01_data_cleaning.ipynb           ← Raw → clean pipeline
│   ├── 02_exploratory_analysis.ipynb    ← EDA: distributions, patterns, gaps
│   └── 03_strategic_scoring.ipynb       ← Scoring model: rank funds by project fit
│
├── 03_powerbi/
│   ├── eif_dashboard.pbix               ← Power BI dashboard (download to view)
│   ├── README.md                        ← Dashboard guide + page descriptions
│   └── screenshots/                     ← Dashboard previews
│
├── 04_business_analysis/
│   ├── opportunity_matrix.xlsx          ← Fund vs. project fit matrix
│   ├── gap_analysis.md                  ← Funding gaps identified
│   └── strategic_recommendations.md    ← Prioritized action plan
│
├── 05_analysis_reports/
│   ├── executive_summary.pdf            ← CEO/COO 1-pager
│   ├── outreach_tracker.pdf             ← Fund manager tracking report
│   └── pitch_deck.pdf                   ← Executive presentation
│
└── docs/
    ├── methodology.md                   ← Research approach and process
    ├── data_dictionary.md               ← Field definitions and data model
    └── decision_framework.md            ← Step-by-step funding eligibility guide
```

---

## Project Overview

### What Was Researched
12 EIF-backed fund managers across Spain, Portugal, Sweden, and globally — covering:
- Private Equity, Venture Capital, Infrastructure, and Debt funds
- Total EIF commitments ranging from €2.8M to €41.2M per intermediary
- SDG-aligned impact funds targeting clean energy, water, and sustainability

### Key Projects This Research Supports
| Project Type | Relevant Funds |
|---|---|
| Solar Energy | Suma Capital, Alantra, NIAM, Axon Partners |
| Green Hydrogen | Suma Capital, Impact Bridge, Axon Partners |
| Desalination / Water | Impact Bridge (SDG 6 & 14), IB Impact Debt |
| Sustainability / ESG | Arta Capital, OXY Capital, Alantra |

---

## How to Navigate This Repo

**If you want the executive overview:**
→ Open `05_analysis_reports/executive_summary.pdf` — a single-page dashboard with all key metrics, rankings, and recommended actions

**If you want the full strategic analysis:**
→ Start with `INSIGHTS.md`, then review `04_business_analysis/strategic_recommendations.md` and `05_analysis_reports/pitch_deck.pdf`

**If you want to explore the data and methodology:**
→ Start with `02_python_analysis/01_data_cleaning.ipynb` through the scoring model, then `docs/methodology.md`

**If you want to check if EU funding applies to your company:**
→ Go to `docs/decision_framework.md` — a 7-step eligibility guide with direct portal links

**If you want the interactive dashboard:**
→ Download `03_powerbi/eif_dashboard.pbix` or browse `03_powerbi/screenshots/` for previews

---

## The Decision Framework (Summary)

A structured 7-step workflow to determine if EU funding applies to your company:

1. **Location check** — EU27, EEA, or outermost regions?
2. **Company category** — Startup, SME, mid-cap, or infrastructure?
3. **Type of finance** — Loans, VC, microfinance, or grants?
4. **Implementing partner** — EIF, EIB, InvestEU, or national banks?
5. **Funding amount** — Under €500K to €50M+?
6. **Sustainability focus** — Which SDGs does your project address?
7. **Output** — Your filtered shortlist + portal link

Full guide: [`docs/decision_framework.md`](docs/decision_framework.md)

---

## Power BI Dashboard

The interactive dashboard includes 6 pages:
- **Overview** — Total funds, countries, EIF commitments, fund types
- **Country Map** — Geographic distribution of intermediaries
- **Fund Type Breakdown** — VC vs PE vs Debt vs Infrastructure
- **SDG Alignment** — Coverage and gaps across 17 SDGs
- **Project Fit Matrix** — Solar / Hydrogen / Desalination vs. each fund
- **Outreach Pipeline** — Status tracker for manager outreach

See [`03_powerbi/README.md`](03_powerbi/README.md) for setup instructions.

---

## Data Source & License

**Source:** European Commission — Your Europe Portal
**URL:** https://youreurope.europa.eu/business/finance-funding/getting-funding/access-finance/en/financial-intermediaries
**Reuse policy:** European Commission reuse policy — public data, reuse permitted
**Collected:** March 2025

---
