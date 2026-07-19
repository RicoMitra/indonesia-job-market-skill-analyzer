# WorkSignal — Job Posting Skill Analyzer

A reproducible, snapshot-based analysis of skills explicitly observed in Indonesian job postings across Data Analyst, Data Scientist, ML Engineer, AI Engineer, Business Analyst, and Software Engineer roles.

The Python pipeline is the source of truth. It cleans CSV data, marks duplicates, maps roles, extracts skills from a transparent regex dictionary, stores results in SQLite, runs exploratory clustering, and exports static JSON summaries. The Next.js interface only renders those summaries; it does not recreate analysis in JavaScript.

> This is an educational sample, not live job-market intelligence, career advice, hiring prediction, or a job-board scraper.

## Refreshing static evidence

To use a free, manually downloaded public snapshot, place one or more CSV files in `pipeline/data/raw/external/`, then run:

```powershell
python pipeline/export_static.py --external pipeline/data/raw/external --public web/public/data
```

The pipeline automatically uses the external CSV files as its primary snapshot when that folder is non-empty. If it is empty, it falls back to the bundled 12-row demo fixture. It accepts common aliases such as `job_title`, `company_name`, `job_location`, `job_description`, `posting_date`, and `job_url`, then normalizes them to `title`, `company`, `location`, `description`, `posted_at`, `source`, `source_url`, and `scraped_at`. Missing fields become empty values (`source` becomes `unknown`) rather than stopping the run. Duplicate postings are removed using `title + company + location + description`.

Download a CSV manually from a source whose license, schema, and source terms you have verified. Do not automate scraping of LinkedIn, Jobstreet, Glints, or Kalibrr. The command regenerates the JSON artifacts and `metadata.json` records source filenames, actual post-deduplication row count, refresh timestamp, and `snapshot dataset, not real-time` status.

## What the snapshot can show

- Most frequently observed explicit skills and role categories.
- Dominant locations and recurring skill combinations.
- Exact-label skill-gap comparison for Data Analyst, Data Scientist, and ML Engineer.
- Evidence rows that retain source and snapshot metadata.

It does **not** measure the full Indonesian market, provide real-time vacancies, predict hiring outcomes, or recommend a career action.

## Data contract and manual refresh

Use a local CSV with `title` and `description`, plus `company`, `location`, `posted_at`, `source`, `source_url`, and `scraped_at` whenever available. The pipeline emits `role_category`, `skills_detected`, and `is_duplicate`, retains one canonical record per stable posting fingerprint, and mirrors static artifacts for Vercel.

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

The active external snapshot is `pipeline/data/raw/external/jobstreet_indonesia_target_roles_5000.csv`: a deterministic 5,000-row target-role subset of the [Jobstreet Indonesia Dataset on Kaggle](https://www.kaggle.com/datasets/azizainunnajib/jobs-crawling), whose public listing reports CC0. It was retrieved from a public BINUS BeeFest dataset mirror on 2026-07-19, normalized to the documented eight-column schema, and then deduplicated by the pipeline. Its dashboard artifact contains 1,991 matched postings after deduplication. This is a historical snapshot, not a claim about the full Indonesian market or current vacancies.

- Role mapping is transparent and title-based; explicitly ambiguous titles can map to more than one role.
- Skill aliases live in `pipeline/src/extract_skills.py`; for example PostgreSQL maps to SQL.
- Skill Gap comparison is descriptive: it only compares exact entered canonical labels against the selected role's Python-generated observed skills.
- KMeans clustering uses a fixed seed and is exploratory. The bundled sample silhouette score is weak, so it should not support strong conclusions.

## Deployment

Deploy `web/` to Vercel with **Root Directory** set to `web`. Commit the generated JSON in `pipeline/outputs/` and `web/public/data/` so Vercel can build the static presentation layer without a Python runtime.

Demo: [WorkSignal on Vercel](https://worksignal-indonesia-job-market-okp8xabox-dan1el.vercel.app)

## Project records

- [AGENTS.md](AGENTS.md) — governance and engineering constraints
- [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) — product and data flow
- [DECISIONS.md](DECISIONS.md) — approved architecture decisions
- [reports/final_report.md](reports/final_report.md) — pipeline sample run
