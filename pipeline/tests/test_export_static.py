import json
from pathlib import Path


def test_export_static_writes_frontend_contract_files(tmp_path):
    from export_static import export_static

    project_root = Path(__file__).resolve().parents[2]
    output_dir = tmp_path / "outputs"
    public_dir = tmp_path / "public-data"

    export_static(
        input_path=project_root / "pipeline" / "data" / "raw" / "sample_jobs.csv",
        processed_dir=tmp_path / "processed",
        output_dir=output_dir,
        public_dir=public_dir,
    )

    expected = {"metadata.json", "overview.json", "roles.json", "role_skills.json", "skill_matrix.json", "clusters.json", "evidence_jobs.json"}
    assert {path.name for path in output_dir.glob("*.json")} == expected
    assert {path.name for path in public_dir.glob("*.json")} == expected

    overview = json.loads((output_dir / "overview.json").read_text(encoding="utf-8"))
    role_skills = json.loads((output_dir / "role_skills.json").read_text(encoding="utf-8"))
    metadata = json.loads((output_dir / "metadata.json").read_text(encoding="utf-8"))
    assert overview["kpis"]["matched_postings"] == 12
    assert "Data Analyst" in role_skills["roles"]
    assert metadata["row_count"] == 12
    assert overview["insights"]["dominant_locations"]
    assert overview["insights"]["skill_combinations"]
