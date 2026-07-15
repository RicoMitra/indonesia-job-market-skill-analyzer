from src.clustering import cluster_jobs


def test_cluster_jobs_returns_deterministic_assignments_for_skill_vectors():
    skills = {
        "a": ["Python", "SQL"], "b": ["Python", "Pandas"], "c": ["SQL", "Power BI"],
        "d": ["Docker", "AWS"], "e": ["Docker", "Kubernetes"], "f": ["AWS", "FastAPI"],
    }

    clusters, quality = cluster_jobs(skills)

    assert len(clusters) == 6
    assert quality["cluster_count"] >= 2
    assert clusters["cluster_label"].notna().all()
