# Project Context

SkillAtlas analyzes public job descriptions for six target roles: Data Analyst, Data Scientist, ML Engineer, AI Engineer, Business Analyst, and Software Engineer. Raw data is normalized, mapped to one or more roles through documented title rules, processed through a regex skill dictionary, and stored in SQLite.

The Streamlit UI is English and uses a job-board-analytics information architecture: filters, evidence, role comparison, exploratory clusters, and a transparent skill-gap explorer. A role count may exceed unique postings because ambiguous titles are intentionally multi-label.

The public default is `data/raw/sample_jobs.csv`, an original illustrative fixture. The candidate larger source is Kaggle's public CC0 Jobstreet Indonesia Dataset. It is not bundled because of its size and must be re-verified for license and schema before download or analysis.
