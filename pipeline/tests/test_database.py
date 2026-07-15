import sqlite3

import pandas as pd

from src.database import build_database, role_skill_summary


def test_database_keeps_multi_role_mappings_and_returns_skill_counts(tmp_path):
    jobs = pd.DataFrame(
        [{"job_id": "a1", "title": "Data & Business Analyst", "company": "Example", "location": "Jakarta", "posted_at": "", "description": "Python and SQL", "source": "sample", "source_url": ""}]
    )
    database_path = tmp_path / "jobs.db"

    build_database(jobs, {"a1": ["Data Analyst", "Business Analyst"]}, {"a1": ["Python", "SQL"]}, database_path)

    with sqlite3.connect(database_path) as connection:
        assert connection.execute("select count(*) from job_roles").fetchone()[0] == 2
    summary = role_skill_summary(database_path, "Data Analyst")
    assert summary.to_dict("records") == [{"skill": "Python", "posting_count": 1}, {"skill": "SQL", "posting_count": 1}]
