"""SQLite storage and read models for the dashboard."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


def build_database(jobs: pd.DataFrame, roles: dict[str, list[str]], skills: dict[str, list[str]], database_path: Path) -> None:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        jobs.to_sql("jobs", connection, if_exists="replace", index=False)
        connection.execute("create table if not exists job_roles (job_id text not null, role text not null)")
        connection.execute("delete from job_roles")
        connection.executemany("insert into job_roles values (?, ?)", [(job_id, role) for job_id, items in roles.items() for role in items])
        connection.execute("create table if not exists job_skills (job_id text not null, skill text not null)")
        connection.execute("delete from job_skills")
        connection.executemany("insert into job_skills values (?, ?)", [(job_id, skill) for job_id, items in skills.items() for skill in items])


def query(database_path: Path, statement: str, params: tuple = ()) -> pd.DataFrame:
    with sqlite3.connect(database_path) as connection:
        return pd.read_sql_query(statement, connection, params=params)


def role_skill_summary(database_path: Path, role: str | None = None) -> pd.DataFrame:
    where = "where jr.role = ?" if role else ""
    params = (role,) if role else ()
    return query(
        database_path,
        f"""
        select js.skill, count(distinct js.job_id) as posting_count
        from job_skills js join job_roles jr on jr.job_id = js.job_id
        {where}
        group by js.skill order by posting_count desc, js.skill asc
        """,
        params,
    )


def role_summary(database_path: Path) -> pd.DataFrame:
    return query(database_path, "select role, count(distinct job_id) as posting_count from job_roles group by role order by posting_count desc, role")
