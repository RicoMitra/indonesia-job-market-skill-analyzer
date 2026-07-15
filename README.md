# Indonesia Job Market Skill Analyzer

An end-to-end, reproducible portfolio project for analyzing job-description skill demand across Data Analyst, Data Scientist, ML Engineer, AI Engineer, Business Analyst, and Software Engineer roles.

It is an educational analysis tool, not live labor-market intelligence, career advice, or a hiring predictor.

## What it demonstrates

- CSV normalization and duplicate removal
- Transparent multi-label role mapping from job titles
- Regex + skill-dictionary extraction with aliases
- SQLite storage and SQL analysis queries
- Exploratory KMeans clustering from extracted skill vectors
- English Streamlit dashboard with filters, evidence tables, role comparison, and skill-gap analysis
- Deterministic tests and a no-auth sample dataset

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m src.pipeline
streamlit run app/streamlit_app.py
```

Open `http://localhost:8501`.

## Quality checks

```bash
python -m pytest tests -q
ruff check .
python -m src.pipeline
```

## Data provenance

`data/raw/sample_jobs.csv` is an original, illustrative fixture included solely so the repository works publicly without credentials. It is not a live market dataset.

The candidate larger Indonesian source is the [Jobstreet Indonesia Dataset on Kaggle](https://www.kaggle.com/datasets/azizainunnajib/jobs-crawling), whose public listing reports a CC0 license and CSV files. Do not treat it as approved automatically: confirm the current license, fields, and source terms at download time; place a full file under `data/raw/full_*.csv`, then run:

```bash
python -m src.pipeline --input data/raw/full_jobs.csv --source jobstreet_indonesia
```

The pipeline expects `title` and `description`; optional canonical fields are `company`, `location`, `posted_at`, and `source_url`. Map external headers before ingestion if necessary. No live scraping, API key, paid API, or LLM is used.

## Method notes

- A job can map to multiple roles when its title is explicitly ambiguous; role counts are therefore not a unique-posting total.
- Skill aliases are defined in `src/extract_skills.py`; for example, PostgreSQL maps to SQL.
- The skill-gap explorer compares entered skills to the selected role’s observed top skills and ranks missing skills by posting frequency.
- Clustering is deterministic (`random_state=42`) but exploratory. The sample’s silhouette score is `0.242`, so it should not be used for strong conclusions.

## Deployment

Deploy this repository to [Streamlit Community Cloud](https://share.streamlit.io/) with `app/streamlit_app.py` as the entry point. Streamlit is the approved deployment target; Vercel does not natively host Streamlit applications.

## Repository guides

- [AGENTS.md](AGENTS.md) — governance
- [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) — product and data flow
- [DECISIONS.md](DECISIONS.md) — approved decisions
- [reports/final_report.md](reports/final_report.md) — sample run results
