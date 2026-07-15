# Decision Log

## D-001: Reproducible batch pipeline

Accepted. CSV ingestion, deterministic processing, SQLite, and Streamlit keep the MVP portable without services.

## D-002: Original public sample fixture

Accepted. The repository includes a small original sample dataset so the project works without source credentials. It is illustrative, not live market data.

## D-003: Public-source candidate

Accepted with verification gate. Kaggle's Jobstreet Indonesia Dataset is a candidate primary source because its public listing states CC0. Its current license, schema, and source terms must be verified again before use. No live scraping is part of this project.

## D-004: Transparent extraction and recommendations

Accepted. Skills use a regex dictionary with aliases; role mapping is title based and multi-label. The skill gap ranks observed missing skills only and makes no hiring prediction.

## D-005: Exploratory clustering

Accepted. KMeans with a fixed seed supports a portfolio demonstration. A weak silhouette score is disclosed instead of overinterpreted.

## D-006: Python-owned static frontend contract

Accepted. The existing Python pipeline remains the only implementation of cleaning, role mapping, skill extraction, SQLite aggregation, and clustering. It exports `overview.json`, `role_skills.json`, `clusters.json`, and `evidence_jobs.json` to `pipeline/outputs/` and mirrors them to `web/public/data/`.

The web UI may render these artifacts and compare exact entered labels to precomputed role skills, but it may not rebuild analysis logic in TypeScript.

## D-007: Next.js frontend deployed from `web/`

Accepted. The portfolio-facing dashboard uses Next.js, Tailwind CSS, and Recharts in `web/` and is deployed to Vercel with that directory as its root. The Streamlit application remains a local reference only.
