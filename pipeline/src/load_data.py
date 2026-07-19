"""Load documented local CSV snapshots into the pipeline's input schema."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


CANONICAL_INPUT_COLUMNS = (
    "title",
    "company",
    "location",
    "description",
    "posted_at",
    "source",
    "source_url",
    "scraped_at",
)

COLUMN_ALIASES = {
    "title": ("title", "job_title", "jobtitle", "position", "role"),
    "company": ("company", "company_name", "employer", "organization"),
    "location": ("location", "job_location", "city", "job_city"),
    "description": ("description", "job_description", "job_desc", "jd", "details"),
    "posted_at": ("posted_at", "posting_date", "posted_date", "date_posted", "date"),
    "source": ("source", "portal", "job_board", "platform"),
    "source_url": ("source_url", "job_url", "url", "link", "posting_url"),
    "scraped_at": ("scraped_at", "retrieved_at", "collected_at", "snapshot_at"),
}


def _normalized_headers(frame: pd.DataFrame) -> pd.DataFrame:
    """Normalize header spelling once, preserving values for deterministic mapping."""
    renamed = {
        column: str(column).strip().lower().replace(" ", "_").replace("-", "_")
        for column in frame.columns
    }
    return frame.rename(columns=renamed)


def normalize_external_csv(raw: pd.DataFrame) -> pd.DataFrame:
    """Map common job-dataset headers and keep unavailable canonical fields empty."""
    raw = _normalized_headers(raw)
    normalized = pd.DataFrame(index=raw.index)
    for canonical, aliases in COLUMN_ALIASES.items():
        matched = next((alias for alias in aliases if alias in raw.columns), None)
        normalized[canonical] = raw[matched] if matched else ""
    normalized = normalized.reindex(columns=CANONICAL_INPUT_COLUMNS).fillna("")
    normalized["source"] = normalized["source"].replace("", "unknown")
    return normalized


def load_job_csvs(fallback_input: Path, external_dir: Path) -> tuple[pd.DataFrame, list[str]]:
    """Use external snapshots when present; otherwise preserve the bundled sample path."""
    files = sorted(external_dir.glob("*.csv")) if external_dir.exists() else []
    if not files:
        return normalize_external_csv(pd.read_csv(fallback_input)), [fallback_input.stem]

    snapshots = [normalize_external_csv(pd.read_csv(path)) for path in files]
    return pd.concat(snapshots, ignore_index=True), [path.stem for path in files]
