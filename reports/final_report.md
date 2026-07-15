# Sample Pipeline Report

## Run

`python -m src.pipeline` against the bundled original sample fixture.

## Result

- Relevant normalized postings: 12
- Role links: 13 (one multi-role title)
- Extracted skill links: 60
- Exploratory clusters: 4
- Silhouette: 0.242

The low silhouette score means the small fixture does not support strong cluster claims. The dashboard labels clusters as exploratory and keeps its primary analysis on transparent role-skill counts.
