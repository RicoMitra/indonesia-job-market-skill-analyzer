"""Export Python pipeline results as static JSON for the Next.js presentation layer."""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

from src.database import query, role_skill_summary, role_summary
from src.pipeline import run


ARTIFACTS = ("overview.json", "role_skills.json", "clusters.json", "evidence_jobs.json")


def records(frame: pd.DataFrame) -> list[dict[str, object]]:
    """Return JSON-safe records without moving analytical logic into the web app."""
    return json.loads(frame.to_json(orient="records"))


def write_json(directory: Path, name: str, payload: dict[str, object]) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / name).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def export_static(input_path: Path, processed_dir: Path, output_dir: Path, public_dir: Path, source: str = "sample") -> dict[str, object]:
    """Run the pipeline, then expose read-only dashboard summaries as JSON files."""
    run(input_path, processed_dir, source=source)
    database = processed_dir / "job_market.db"
    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    roles = role_summary(database)
    all_skills = role_skill_summary(database).head(12)
    evidence = query(
        database,
        """
        select j.job_id, j.title, j.company, j.location, j.posted_at,
               group_concat(jr.role, ' | ') as roles
        from jobs j
        left join job_roles jr on jr.job_id = j.job_id
        group by j.job_id, j.title, j.company, j.location, j.posted_at
        order by j.posted_at desc, j.title asc
        """,
    )
    role_skills = {
        role: records(role_skill_summary(database, role).head(15))
        for role in roles["role"].tolist()
    }
    cluster_rows = query(
        database,
        """
        select cluster, cluster_label, count(*) as posting_count
        from job_clusters
        group by cluster, cluster_label
        order by posting_count desc, cluster asc
        """,
    )
    clusters = [
        {
            "id": int(row.cluster),
            "label": row.cluster_label,
            "posting_count": int(row.posting_count),
            "defining_skills": [skill.strip() for skill in row.cluster_label.split("/")],
        }
        for row in cluster_rows.itertuples()
    ]
    overview = {
        "generated_at": generated_at,
        "source": {
            "name": "Bundled illustrative public sample",
            "type": "Original demo fixture",
            "disclosure": "This is a reproducible educational snapshot, not live job-market intelligence.",
        },
        "kpis": {
            "matched_postings": int(query(database, "select count(*) as count from jobs").iloc[0]["count"]),
            "roles_covered": int(len(roles)),
            "top_observed_skill": all_skills.iloc[0].skill if not all_skills.empty else None,
        },
        "top_skills": records(all_skills),
        "role_comparison": records(roles),
    }
    write_json(output_dir, "overview.json", overview)
    write_json(output_dir, "role_skills.json", {"generated_at": generated_at, "roles": role_skills})
    write_json(output_dir, "clusters.json", {"generated_at": generated_at, "exploratory": True, "clusters": clusters})
    write_json(output_dir, "evidence_jobs.json", {"generated_at": generated_at, "jobs": records(evidence)})
    public_dir.mkdir(parents=True, exist_ok=True)
    for artifact in ARTIFACTS:
        shutil.copy2(output_dir / artifact, public_dir / artifact)
    return overview


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("pipeline/data/raw/sample_jobs.csv"))
    parser.add_argument("--processed", type=Path, default=Path("pipeline/data/processed"))
    parser.add_argument("--output", type=Path, default=Path("pipeline/outputs"))
    parser.add_argument("--public", type=Path, default=Path("web/public/data"))
    parser.add_argument("--source", default="sample")
    args = parser.parse_args()
    print(export_static(args.input, args.processed, args.output, args.public, args.source)["kpis"])
