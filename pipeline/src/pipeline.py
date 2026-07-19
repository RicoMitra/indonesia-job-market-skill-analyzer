"""Rebuild all generated portfolio artifacts from a CSV source."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.clean_data import clean_jobs
from src.clustering import cluster_jobs
from src.database import build_database
from src.extract_skills import extract_skills
from src.roles import map_roles


def run(input_path: Path, output_dir: Path, source: str = "sample") -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    jobs = clean_jobs(pd.read_csv(input_path), source=source)
    role_map = {row.job_id: map_roles(row.title) for row in jobs.itertuples()}
    role_map = {job_id: roles for job_id, roles in role_map.items() if roles}
    jobs = jobs[jobs.job_id.isin(role_map)].copy()
    skill_map = {row.job_id: extract_skills(row.description) for row in jobs.itertuples()}
    jobs["role_category"] = jobs["job_id"].map(lambda job_id: " | ".join(role_map[job_id]))
    jobs["skills_detected"] = jobs["job_id"].map(lambda job_id: " | ".join(skill_map[job_id]))
    build_database(jobs, role_map, skill_map, output_dir / "job_market.db")
    clusters, quality = cluster_jobs(skill_map)
    if not clusters.empty:
        clusters.to_sql("job_clusters", __import__("sqlite3").connect(output_dir / "job_market.db"), if_exists="replace", index=False)
    jobs.to_csv(output_dir / "jobs_normalized.csv", index=False)
    return {"jobs": len(jobs), "role_links": sum(map(len, role_map.values())), "skills": sum(map(len, skill_map.values())), **quality}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("pipeline/data/raw/sample_jobs.csv"))
    parser.add_argument("--output", type=Path, default=Path("pipeline/data/processed"))
    parser.add_argument("--out", type=Path, help="Optional static JSON directory for the Next.js interface")
    parser.add_argument("--source", default="sample")
    args = parser.parse_args()
    if args.out:
        from export_static import export_static

        print(export_static(args.input, args.output, Path("pipeline/outputs"), args.out, args.source)["kpis"])
    else:
        print(run(args.input, args.output, args.source))
