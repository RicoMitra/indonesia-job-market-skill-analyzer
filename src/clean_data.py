"""Normalize public job-posting data into a portable schema."""

from __future__ import annotations

import hashlib
import re

import pandas as pd


CANONICAL_COLUMNS = ["job_id", "title", "company", "location", "posted_at", "description", "source", "source_url"]


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
    jobs["source"] = source
    jobs["posted_at"] = jobs.get("posted_at", "")
    jobs["source_url"] = jobs.get("source_url", "")
    fingerprint = jobs[["title", "company", "location", "description"]].agg("|".join, axis=1)
    jobs["job_id"] = fingerprint.map(lambda value: hashlib.sha1(value.lower().encode()).hexdigest()[:16])
    jobs = jobs.drop_duplicates("job_id")
    return jobs.reindex(columns=CANONICAL_COLUMNS).reset_index(drop=True)
