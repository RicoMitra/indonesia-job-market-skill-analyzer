from pathlib import Path

import streamlit as st

from src.database import query, role_skill_summary, role_summary
from src.recommend import skill_gap


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "data" / "processed" / "job_market.db"
ROLES = ["All roles", "Data Analyst", "Data Scientist", "ML Engineer", "AI Engineer", "Business Analyst", "Software Engineer"]

st.set_page_config(page_title="SkillAtlas | Job market evidence", page_icon="◌", layout="wide")
st.markdown("""<style>
.stApp{background:#f7f6f0;color:#17201c}[data-testid='stSidebar']{background:#eef1e9}
h1,h2,h3{color:#17201c!important}.stButton button{border-radius:999px;border-color:#237a57;color:#18583e}
</style>""", unsafe_allow_html=True)


@st.cache_data
def locations() -> list[str]:
    return query(DATABASE, "select distinct location from jobs where location <> '' order by location")["location"].tolist()


def filtered_jobs(role: str, location: str):
    clauses, params = [], []
    if role != "All roles":
        clauses.append("jr.role = ?")
        params.append(role)
    if location != "All locations":
        clauses.append("j.location = ?")
        params.append(location)
    where = f"where {' and '.join(clauses)}" if clauses else ""
    return query(DATABASE, f"select distinct j.* from jobs j left join job_roles jr on jr.job_id=j.job_id {where} order by j.posted_at desc", tuple(params))


if not DATABASE.exists():
    st.error("No processed database found. Run `python -m src.pipeline` from the repository root.")
    st.stop()

with st.sidebar:
    st.title("SkillAtlas")
    st.caption("Job-market evidence, not career advice.")
    page = st.radio("Explore", ["Overview", "Roles", "Clusters", "Skill Gap", "Methods"])
    role = st.selectbox("Role filter", ROLES)
    location = st.selectbox("Location", ["All locations", *locations()])

jobs = filtered_jobs(role, location)

if page == "Overview":
    st.title("Data roles, decoded")
    st.caption("A reproducible snapshot of publicly described job requirements. Counts reflect selected filters.")
    skills = role_skill_summary(DATABASE, None if role == "All roles" else role)
    a, b, c = st.columns(3)
    a.metric("Matched postings", len(jobs))
    b.metric("Roles covered", len(role_summary(DATABASE)))
    c.metric("Top observed skill", skills.iloc[0].skill if not skills.empty else "—")
    st.divider()
    left, right = st.columns([1.25, 1])
    with left:
        st.subheader("Top skills by role")
        st.bar_chart(skills.head(12).set_index("skill"))
        st.dataframe(skills.head(12), hide_index=True, use_container_width=True)
    with right:
        st.subheader("Role comparison")
        st.dataframe(role_summary(DATABASE), hide_index=True, use_container_width=True)
        st.subheader("Recent evidence")
        st.dataframe(jobs[["title", "company", "location", "posted_at"]].head(6), hide_index=True, use_container_width=True)

elif page == "Roles":
    st.title("Role comparison")
    selected = role if role != "All roles" else st.selectbox("Select a role", ROLES[1:])
    skills = role_skill_summary(DATABASE, selected)
    st.caption(f"Skills are counted once per posting for **{selected}**.")
    st.bar_chart(skills.head(15).set_index("skill"))
    st.dataframe(skills, hide_index=True, use_container_width=True)

elif page == "Clusters":
    st.title("Exploratory job clusters")
    try:
        clusters = query(DATABASE, "select cluster, cluster_label, count(*) as posting_count from job_clusters group by cluster, cluster_label order by posting_count desc")
    except Exception:
        clusters = None
    if clusters is None or clusters.empty:
        st.info("The dataset is too small or homogeneous for a useful exploratory cluster. Core analysis remains available.")
    else:
        st.caption("Clusters are derived from overlapping extracted skills; labels show common skills, not job categories.")
        st.bar_chart(clusters.set_index("cluster_label")[["posting_count"]])
        st.dataframe(clusters, hide_index=True, use_container_width=True)

elif page == "Skill Gap":
    st.title("Skill gap explorer")
    target = st.selectbox("Target role", ROLES[1:])
    entered = st.text_input("Your skills", placeholder="Python, SQL, Docker")
    st.caption("Missing skills are commonly observed in this dataset—not a hiring guarantee.")
    if entered:
        result = skill_gap(entered.split(","), role_skill_summary(DATABASE, target).head(12))
        st.metric("Observed skill coverage", f"{result['coverage_percent']:.1f}%")
        one, two = st.columns(2)
        one.subheader("Matched")
        one.write(", ".join(result["matched"]) or "No recognized skills from this role’s observed list.")
        two.subheader("Missing to explore")
        two.write(", ".join(result["missing"]) or "You cover the displayed skills.")
    else:
        st.info("Enter comma-separated skills to compare them against the selected role.")

else:
    st.title("Method and data notes")
    st.markdown("""- **Source:** bundled original sample data for a no-auth demo; larger public sources must be downloaded separately and documented before ingestion.
- **Roles:** transparent title rules; ambiguous titles may map to multiple roles.
- **Skills:** a regex dictionary with aliases such as PostgreSQL → SQL.
- **Clusters:** deterministic KMeans (`random_state=42`) on extracted-skill presence; weak results remain exploratory.
- **Privacy:** this app sends no data to external services.
""")
