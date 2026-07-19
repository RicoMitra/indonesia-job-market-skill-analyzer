"""Normalize public job-posting data into a portable schema."""

from __future__ import annotations

import hashlib
import re

import pandas as pd


CANONICAL_COLUMNS = ["job_id", "title", "company", "location", "posted_at", "description", "source", "source_url", "scraped_at", "role_category", "skills_detected", "is_duplicate"]


def _text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def clean_jobs(raw: pd.DataFrame, source: str) -> pd.DataFrame:
    """Return unique, non-empty job descriptions with stable local IDs."""
    jobs = raw.copy()
    for column in ["title", "company", "location", "description"]:
        if column not in jobs:
            jobs[column] = ""
        jobs[column] = jobs[column].map(_text)
    jobs = jobs[jobs["description"].ne("")].copy()
    if "source" not in jobs:
        jobs["source"] = source
    else:
        jobs["source"] = jobs["source"].replace("", source).fillna(source)
    jobs["posted_at"] = jobs.get("posted_at", "")
    jobs["source_url"] = jobs.get("source_url", "")
    jobs["scraped_at"] = jobs.get("scraped_at", "")
    jobs["role_category"] = jobs.get("role_category", "")
    jobs["skills_detected"] = jobs.get("skills_detected", "")
    fingerprint = jobs[["title", "company", "location", "description"]].agg("|".join, axis=1)
    jobs["job_id"] = fingerprint.map(lambda value: hashlib.sha1(value.lower().encode()).hexdigest()[:16])
    jobs["is_duplicate"] = jobs.duplicated("job_id", keep="first")
    jobs = jobs[~jobs["is_duplicate"]].copy()
    return jobs.reindex(columns=CANONICAL_COLUMNS).reset_index(drop=True)
