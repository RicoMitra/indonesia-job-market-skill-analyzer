from pathlib import Path

import pandas as pd


def test_external_csv_becomes_the_primary_input_and_normalizes_aliases(tmp_path):
    from src.load_data import load_job_csvs

    external_dir = tmp_path / "external"
    external_dir.mkdir()
    pd.DataFrame(
        [
            {
                "job_title": "Data Analyst",
                "company_name": "Example Co",
                "job_location": "Jakarta",
                "job_description": "Use SQL and Python to analyse product data.",
                "posting_date": "2026-01-01",
                "job_url": "https://example.test/jobs/1",
            },
            {
                "job_title": "Software Engineer",
                "job_description": "Build web services with Python and Docker.",
            },
        ]
    ).to_csv(external_dir / "manual_snapshot.csv", index=False)

    jobs, sources = load_job_csvs(
        fallback_input=Path("pipeline/data/raw/sample_jobs.csv"), external_dir=external_dir
    )

    assert len(jobs) == 2
    assert sources == ["manual_snapshot"]
    assert jobs.loc[0, "title"] == "Data Analyst"
    assert jobs.loc[0, "company"] == "Example Co"
    assert jobs.loc[0, "location"] == "Jakarta"
    assert jobs.loc[0, "description"].startswith("Use SQL")
    assert jobs.loc[0, "posted_at"] == "2026-01-01"
    assert jobs.loc[0, "source"] == "unknown"
    assert jobs.loc[0, "source_url"] == "https://example.test/jobs/1"
    assert jobs.loc[1, "company"] == ""
    assert jobs.loc[1, "scraped_at"] == ""


def test_loader_falls_back_to_bundled_sample_when_external_folder_is_empty(tmp_path):
    from src.load_data import load_job_csvs

    jobs, sources = load_job_csvs(
        fallback_input=Path("pipeline/data/raw/sample_jobs.csv"), external_dir=tmp_path / "external"
    )

    assert len(jobs) == 12
    assert sources == ["sample_jobs"]


def test_normalize_external_csv_supports_jobstreet_camel_case_headers():
    from src.load_data import normalize_external_csv

    result = normalize_external_csv(
        pd.DataFrame(
            [
                {
                    "jobTitle": "Data Analyst",
                    "companyName": "Example Co",
                    "locations": "Jakarta",
                    "description": "Use SQL and Python.",
                    "postedAt": "2021-12-12T17:00:00Z",
                    "jobUrl": "https://example.test/jobs/1",
                }
            ]
        )
    )

    assert result.loc[0, "company"] == "Example Co"
    assert result.loc[0, "location"] == "Jakarta"
    assert result.loc[0, "posted_at"] == "2021-12-12T17:00:00Z"
    assert result.loc[0, "source_url"] == "https://example.test/jobs/1"


def test_export_static_reports_external_snapshot_metadata(tmp_path):
    from export_static import export_static

    external_dir = tmp_path / "external"
    external_dir.mkdir()
    pd.DataFrame(
        [
            {
                "title": "Data Scientist",
                "company": "Example Co",
                "location": "Bandung",
                "description": "Use Python, SQL, and machine learning.",
                "source": "manual public snapshot",
                "scraped_at": "2026-07-19T00:00:00Z",
            },
            {
                "title": "Data Scientist",
                "company": "Example Co",
                "location": "Bandung",
                "description": "Use Python, SQL, and machine learning.",
                "source": "manual public snapshot",
            },
        ]
    ).to_csv(external_dir / "verified_snapshot.csv", index=False)

    export_static(
        input_path=Path("pipeline/data/raw/sample_jobs.csv"),
        processed_dir=tmp_path / "processed",
        output_dir=tmp_path / "outputs",
        public_dir=tmp_path / "public",
        external_dir=external_dir,
    )

    import json

    metadata = json.loads((tmp_path / "outputs" / "metadata.json").read_text(encoding="utf-8"))
    overview = json.loads((tmp_path / "outputs" / "overview.json").read_text(encoding="utf-8"))
    assert metadata["row_count"] == 1
    assert metadata["source_name"] == "manual public snapshot"
    assert metadata["source_datasets"] == ["verified_snapshot"]
    assert metadata["status"] == "snapshot dataset, not real-time"
    assert metadata["retrieval_date"] == "2026-07-19T00:00:00Z"
    assert metadata["license"] == "Verify the license and source terms for each manually supplied external snapshot."
    assert overview["source"]["name"] == "manual public snapshot"
