# Project Governance

## Owner

Rico Majesty Daniel Mitra ([@RicoMitra](https://github.com/RicoMitra)).

## Purpose

Build a lightweight, educational job-market analytics portfolio project. It analyzes documented public job-posting data to explain observed skill demand across selected roles. It is not a recruiting platform, live labor-market feed, or career-outcome predictor.

## Stack and constraints

- Data engine: Python 3.11+, pandas, scikit-learn, and SQLite under `pipeline/`.
- Web dashboard: Next.js, TypeScript, Tailwind CSS, and Recharts under `web/`.
- Streamlit remains a legacy local reference; Vercel deploys the `web/` frontend.
- Public, documented data only. Bundle an original sample CSV for no-auth reproducibility.
- No live scraping, paid APIs, accounts, LLM dependency, or unnecessary services.
- Keep the pipeline deterministic, typed where practical, and testable.
- Keep source data provenance, license, schema, retrieval date, and limitations visible.
- Export Python-owned static summaries to `pipeline/outputs/` and mirror them to `web/public/data/`. TypeScript may render those artifacts and perform exact label comparison for the Skill Gap view, but must not recreate data cleaning, role mapping, skill extraction, SQL aggregation, or clustering.

## Decisions

The owner must approve changes to data source licensing, public-facing claims, analytics semantics, major dependencies, or deployment architecture. Prefer the smallest reversible solution otherwise.
