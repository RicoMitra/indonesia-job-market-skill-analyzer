from pathlib import Path

from src.runtime import ensure_database


def test_ensure_database_builds_missing_database_from_sample(tmp_path):
    source = Path(__file__).resolve().parents[1] / "data" / "raw" / "sample_jobs.csv"
    database = tmp_path / "processed" / "job_market.db"

    created = ensure_database(source, database)

    assert created is True
    assert database.exists()
