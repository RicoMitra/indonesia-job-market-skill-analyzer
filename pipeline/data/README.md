# Data Notes

## Bundled source

`raw/sample_jobs.csv` is an original illustrative sample written for this repository. Its schema is verified by `src.clean_data.clean_jobs` and includes the required `title` and `description` columns plus optional company, location, date, and URL fields. It is public within this repository and requires no account, key, or invitation.

## Active external source

`raw/external/jobstreet_indonesia_target_roles_5000.csv` is a deterministic 5,000-row target-role subset built on 2026-07-19 from the public [Jobstreet Indonesia Dataset](https://www.kaggle.com/datasets/azizainunnajib/jobs-crawling) mirror linked by BINUS BeeFest. Kaggle's public listing reports CC0. The source schema was verified as `jobTitle`, `companyName`, `locations`, `description`, `postedAt`, and `jobUrl` before normalization. The stored snapshot uses the standard eight-column schema and removes query-string parameters from public job URLs. The larger 623,610-row download remains local-only; generated dashboard evidence reflects the deduplicated target-role snapshot.

## Adding a manual external snapshot

1. Download a CSV manually from a verified free/public source. Do not run a portal scraper from this repository.
2. Put the CSV in `raw/external/`. Every `*.csv` file in that folder becomes the primary input; the 12-row bundled demo is used only when the folder is empty.
3. The loader accepts standard fields and common aliases, including `job_title`, `company_name`, `job_location`, `job_description`, `posting_date`, and `job_url`. It fills absent optional fields with empty values and defaults a missing `source` to `unknown`.
4. From the repository root, run `python pipeline/export_static.py --external pipeline/data/raw/external --public web/public/data`.

`metadata.json` then reports source filename(s), the deduplicated posting count, refresh time, and `snapshot dataset, not real-time`. A CSV without usable descriptions will not create role-skill evidence, but it will not cause a schema error.

## Generated files

`processed/` is created by `python -m src.pipeline` and is intentionally ignored by Git. It contains the SQLite database and normalized output derived from the local source file.
