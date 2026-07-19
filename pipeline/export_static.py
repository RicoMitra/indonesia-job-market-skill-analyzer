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


ARTIFACTS = ("metadata.json", "overview.json", "roles.json", "role_skills.json", "skill_matrix.json", "clusters.json", "evidence_jobs.json")


def records(frame: pd.DataFrame) -> list[dict[str, object]]:
    """Return JSON-safe records without moving analytical logic into the web app."""
    return json.loads(frame.to_json(orient="records"))


def write_json(directory: Path, name: str, payload: dict[str, object]) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / name).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def export_static(
    input_path: Path,
    processed_dir: Path,
    output_dir: Path,
    public_dir: Path,
    source: str = "sample",
    external_dir: Path = Path("pipeline/data/raw/external"),
) -> dict[str, object]:
    """Run the pipeline, then expose read-only dashboard summaries as JSON files."""
    pipeline_result = run(input_path, processed_dir, source=source, external_dir=external_dir)
    database = processed_dir / "job_market.db"
    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    is_external_snapshot = pipeline_result["source_datasets"] != [input_path.stem]
    roles = role_summary(database)
    all_skills = role_skill_summary(database).head(12)
    retrieval_date = query(
        database, "select max(nullif(trim(scraped_at), '')) as value from jobs"
    ).iloc[0]["value"]
    source_names = query(
        database, "select distinct source from jobs where trim(source) <> '' order by source"
    )["source"].tolist()
    source_name = " + ".join(source_names) if source_names else "unknown"
    evidence = query(
        database,
        """
        select j.job_id, j.title, j.company, j.location, j.posted_at, j.source, j.scraped_at,
               group_concat(distinct jr.role) as roles,
               group_concat(distinct js.skill) as skills_detected
        from jobs j
        left join job_roles jr on jr.job_id = j.job_id
        left join job_skills js on js.job_id = j.job_id
        group by j.job_id, j.title, j.company, j.location, j.posted_at, j.source, j.scraped_at
        order by j.posted_at desc, j.title asc
        """,
    )
    role_skills = {
        role: records(role_skill_summary(database, role).head(15))
        for role in roles["role"].tolist()
    }
    metadata = {
        "generated_at": generated_at,
        "source": source_name,
        "source_name": source_name,
        "source_datasets": pipeline_result["source_datasets"],
        "license": "Verify the license and source terms for each manually supplied external snapshot."
        if is_external_snapshot
        else "Original demo fixture; replace through the documented local CSV refresh workflow.",
        "row_count": int(query(database, "select count(*) as count from jobs").iloc[0]["count"]),
        "refresh_date": generated_at,
        "retrieval_date": retrieval_date,
        "status": "snapshot dataset, not real-time",
        "limitations": "Static educational sample. No live scraping, paid API, or career advice.",
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
    locations = query(
        database,
        "select location, count(*) as posting_count from jobs where trim(location) <> '' group by location order by posting_count desc, location limit 5",
    )
    skill_pairs = query(
        database,
        """
        select a.skill as skill_a, b.skill as skill_b, count(distinct a.job_id) as posting_count
        from job_skills a join job_skills b on a.job_id = b.job_id and a.skill < b.skill
        group by a.skill, b.skill order by posting_count desc, skill_a, skill_b limit 5
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
            "name": source_name,
            "type": "External local snapshot" if is_external_snapshot else "Original demo fixture",
            "disclosure": "This is a reproducible snapshot dataset, not a real-time job-market feed.",
        },
        "kpis": {
            "matched_postings": int(query(database, "select count(*) as count from jobs").iloc[0]["count"]),
            "roles_covered": int(len(roles)),
            "top_observed_skill": all_skills.iloc[0].skill if not all_skills.empty else None,
        },
        "top_skills": records(all_skills),
        "role_comparison": records(roles),
        "insights": {
            "dominant_locations": records(locations),
            "skill_combinations": records(skill_pairs),
            "warning": "Observed posting frequency is descriptive evidence, not a real-time market estimate or career recommendation.",
        },
    }
    write_json(output_dir, "overview.json", overview)
    write_json(output_dir, "metadata.json", metadata)
    write_json(output_dir, "roles.json", {"generated_at": generated_at, "roles": records(roles)})
    write_json(output_dir, "role_skills.json", {"generated_at": generated_at, "roles": role_skills})
    write_json(output_dir, "skill_matrix.json", {"generated_at": generated_at, "roles": role_skills, "skills": sorted({item["skill"] for values in role_skills.values() for item in values})})
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
    parser.add_argument("--external", type=Path, default=Path("pipeline/data/raw/external"))
    args = parser.parse_args()
    print(export_static(args.input, args.processed, args.output, args.public, args.source, args.external)["kpis"])
