# Project Governance

## Owner

Rico Majesty Daniel Mitra ([@RicoMitra](https://github.com/RicoMitra)).

## Purpose

Build a lightweight, educational job-market analytics portfolio project. It analyzes documented public job-posting data to explain observed skill demand across selected roles. It is not a recruiting platform, live labor-market feed, or career-outcome predictor.

## Stack and constraints

- Python 3.11+, pandas, scikit-learn, SQLite, and Streamlit.
- Public, documented data only. Bundle an original sample CSV for no-auth reproducibility.
- No live scraping, paid APIs, accounts, LLM dependency, or unnecessary services.
- Keep the pipeline deterministic, typed where practical, and testable.
- Keep source data provenance, license, schema, retrieval date, and limitations visible.

## Decisions

The owner must approve changes to data source licensing, public-facing claims, analytics semantics, major dependencies, or deployment architecture. Prefer the smallest reversible solution otherwise.
