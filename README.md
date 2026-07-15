# SkillAtlas — Indonesia Job Market Skill Analyzer

A reproducible data product that examines skills explicitly observed in Indonesian job-description samples across Data Analyst, Data Scientist, ML Engineer, AI Engineer, Business Analyst, and Software Engineer roles.

The Python pipeline is the source of truth. It cleans CSV data, maps roles, extracts skills from a transparent regex dictionary, stores results in SQLite, runs exploratory clustering, and exports static JSON summaries. The Next.js dashboard only renders those summaries; it does not recreate analysis in JavaScript.

> This is an educational sample, not live job-market intelligence, career advice, hiring prediction, or a job-board scraper.

## Product views

- **Overview:** KPI, source disclosure, top observed skills, role comparison, and sample evidence rows.
- **Roles:** role selector, skill-frequency chart, and corresponding evidence postings.
- **Clusters:** exploratory cluster cards with defining observed skills.
- **Skill Gap:** exact input-to-precomputed-skill comparison with coverage, matches, and missing skills.
- **Methods:** dataset, pipeline, mapping, dictionary, and limitation disclosure.

## Architecture

```text
pipeline/
  src/                 Python data engine
  data/                Original sample + ignored processed SQLite artifacts
  outputs/             Versioned JSON contract from Python
  export_static.py     Rebuilds analysis and frontend JSON
web/
  app/ components/     Next.js presentation layer
  lib/                 JSON loading and types
  public/data/         Mirrored Python JSON for static deployment
```

## Local setup

### 1. Run the Python data engine

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python pipeline\export_static.py
```

This rebuilds SQLite and normalized CSV files under `pipeline/data/processed/`, then writes and mirrors these static contracts:

- `overview.json`
- `role_skills.json`
- `clusters.json`
- `evidence_jobs.json`

### 2. Run the web dashboard

```powershell
cd web
pnpm install
pnpm dev
```

Open `http://localhost:3000`.

## Verification

```powershell
python -m pytest -q
ruff check .
python pipeline\export_static.py
cd web
pnpm typecheck
pnpm lint
pnpm build
```

## Data provenance and limitations

`pipeline/data/raw/sample_jobs.csv` is an original, illustrative fixture included so the repository works without credentials or scraping. It is not a live labor-market dataset.

The candidate larger Indonesian source is the [Jobstreet Indonesia Dataset on Kaggle](https://www.kaggle.com/datasets/azizainunnajib/jobs-crawling), whose public listing previously reported CC0. Its license, schema, retrieval date, and source terms must be checked again before it is used. The pipeline needs `title` and `description`; optional canonical fields are `company`, `location`, `posted_at`, and `source_url`.

- Role mapping is transparent and title-based; explicitly ambiguous titles can map to more than one role.
- Skill aliases live in `pipeline/src/extract_skills.py`; for example PostgreSQL maps to SQL.
- Skill Gap comparison is descriptive: it only compares exact entered canonical labels against the selected role's Python-generated observed skills.
- KMeans clustering uses a fixed seed and is exploratory. The bundled sample silhouette score is weak, so it should not support strong conclusions.

## Deployment

Deploy `web/` to Vercel with **Root Directory** set to `web`. Commit the generated JSON in `pipeline/outputs/` and `web/public/data/` so Vercel can build the static presentation layer without a Python runtime.

## Project records

- [AGENTS.md](AGENTS.md) — governance and engineering constraints
- [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) — product and data flow
- [DECISIONS.md](DECISIONS.md) — approved architecture decisions
- [reports/final_report.md](reports/final_report.md) — pipeline sample run
