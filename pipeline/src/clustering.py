"""Exploratory, deterministic clustering from extracted skills."""

from __future__ import annotations

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics import silhouette_score


def cluster_jobs(job_skills: dict[str, list[str]]) -> tuple[pd.DataFrame, dict[str, float | int]]:
    rows = [{skill: 1 for skill in skills} for skills in job_skills.values() if skills]
    ids = [job_id for job_id, skills in job_skills.items() if skills]
    if len(rows) < 6 or len({tuple(sorted(row)) for row in rows}) < 3:
        return pd.DataFrame(columns=["job_id", "cluster", "cluster_label"]), {"cluster_count": 0, "silhouette": 0.0}
    matrix = DictVectorizer(sparse=True).fit_transform(rows)
    # scikit-learn on this Windows build rejects SciPy's default int64 sparse indices.
    matrix.indices = matrix.indices.astype("int32")
    matrix.indptr = matrix.indptr.astype("int32")
    cluster_count = min(4, len(rows) - 1, matrix.shape[0] - 1)
    model = KMeans(n_clusters=cluster_count, random_state=42, n_init=10)
    labels = model.fit_predict(matrix)
    score = float(silhouette_score(matrix, labels)) if len(set(labels)) > 1 else 0.0
    # Reuse each cluster's observed skill frequency, avoiding opaque model-weight names.
    frame = pd.DataFrame({"job_id": ids, "cluster": labels})
    label_map = {}
    for cluster in sorted(frame.cluster.unique()):
        selected = [rows[index] for index, value in enumerate(labels) if value == cluster]
        counts = pd.Series([skill for row in selected for skill in row]).value_counts()
        label_map[cluster] = " / ".join(counts.index[:3])
    frame["cluster_label"] = frame["cluster"].map(label_map)
    return frame, {"cluster_count": int(cluster_count), "silhouette": round(score, 3)}
