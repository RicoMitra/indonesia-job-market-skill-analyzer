# Data Notes

## Bundled source

`raw/sample_jobs.csv` is an original illustrative sample written for this repository. Its schema is verified by `src.clean_data.clean_jobs` and includes the required `title` and `description` columns plus optional company, location, date, and URL fields. It is public within this repository and requires no account, key, or invitation.

## Candidate external source

Kaggle's [Jobstreet Indonesia Dataset](https://www.kaggle.com/datasets/azizainunnajib/jobs-crawling) is a potential larger source. Its public listing reported a CC0 license and dated CSV files when this project was designed. It is not ingested or redistributed here. Before any use, re-check the listing's license, inspect the downloaded headers for `title` and a full description-equivalent field, document the retrieval date, and confirm source terms.

## Generated files

`processed/` is created by `python -m src.pipeline` and is intentionally ignored by Git. It contains the SQLite database and normalized output derived from the local source file.
