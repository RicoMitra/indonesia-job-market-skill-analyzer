from pathlib import Path

import streamlit as st

from bootstrap import add_project_root

add_project_root()

from src.database import query, role_skill_summary, role_summary  # noqa: E402
from src.recommend import skill_gap  # noqa: E402
from src.runtime import ensure_database  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "pipeline" / "data" / "processed" / "job_market.db"
SAMPLE = ROOT / "pipeline" / "data" / "raw" / "sample_jobs.csv"
ROLES = ["All roles", "Data Analyst", "Data Scientist", "ML Engineer", "AI Engineer", "Business Analyst", "Software Engineer"]

st.set_page_config(page_title="SkillAtlas | Job market evidence", layout="wide", initial_sidebar_state="expanded")
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
:root { --paper:#f5f3ed; --panel:#fcfbf7; --ink:#17201c; --muted:#68736b; --line:#d8ded5; --forest:#153b2b; --emerald:#207451; --soft:#e8f1e9; }
.stApp { background:var(--paper); color:var(--ink); font-family:'Plus Jakarta Sans',sans-serif; }
[data-testid='stHeader'] { background:rgba(245,243,237,.9); }
.block-container { max-width:1420px; min-width:0; padding:2.75rem 3rem 4rem; }
[data-testid='stSidebar'] { background:var(--forest); border-right:1px solid rgba(255,255,255,.1); }
[data-testid='stSidebar'] { color:#f5f7f2; }
[data-testid='stSidebar'] h1, [data-testid='stSidebar'] p, [data-testid='stSidebar'] label, [data-testid='stSidebar'] [data-testid='stCaptionContainer'] { color:#f5f7f2 !important; }
[data-testid='stSidebar'] [data-baseweb='select'] > div { background:#f7f8f4; border:1px solid #8aa294; border-radius:10px; }
[data-testid='stSidebar'] [data-baseweb='select'] * { color:var(--ink) !important; }
[data-testid='stSidebar'] [data-baseweb='select'] input { color:var(--ink) !important; -webkit-text-fill-color:var(--ink) !important; opacity:1 !important; }
[data-testid='stSidebar'] [data-baseweb='select'] span { color:var(--ink) !important; }
[data-testid='stSidebar'] [role='radiogroup'] { gap:.25rem; }
[data-testid='stSidebar'] label { padding:.55rem .65rem; border-radius:8px; transition:background 160ms cubic-bezier(.23,1,.32,1); }
[data-testid='stSidebar'] label:hover { background:rgba(232,241,233,.15); }
h1,h2,h3,p { color:var(--ink); }
h1 { font-size:clamp(2rem,4vw,3.2rem) !important; letter-spacing:-.065em; line-height:1.04; font-weight:800; margin-bottom:.35rem !important; }
h2 { font-size:1.2rem !important; letter-spacing:-.035em; font-weight:750; margin-top:0 !important; }
h3 { font-size:.85rem !important; letter-spacing:.08em; text-transform:uppercase; font-weight:800; color:#496256 !important; }
.stCaption, [data-testid='stCaptionContainer'] p { color:var(--muted) !important; line-height:1.55; }
.stDivider { border-color:var(--line); margin:2rem 0 !important; }
.hero { border-bottom:1px solid var(--line); padding:0 0 1.8rem; margin-bottom:1.6rem; }
.eyebrow { color:var(--emerald); font:500 .69rem/1 'DM Mono',monospace; letter-spacing:.14em; text-transform:uppercase; margin-bottom:.85rem; }
.lede { color:var(--muted); max-width:63ch; font-size:1rem; line-height:1.65; margin:0; }
.badge-row { display:flex; flex-wrap:wrap; gap:.5rem; margin-top:1.2rem; }
.badge { display:inline-flex; border:1px solid #b7c8bb; background:#edf3ed; border-radius:999px; padding:.34rem .62rem; color:#2c5c43; font:500 .68rem/1 'DM Mono',monospace; }
.metric-card { background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:1.05rem 1.15rem 1.15rem; min-height:124px; box-shadow:0 14px 30px -25px rgba(27,57,41,.28); }
.metric-label { color:var(--muted); font:500 .68rem/1 'DM Mono',monospace; letter-spacing:.08em; text-transform:uppercase; }
.metric-value { color:var(--ink); font-size:2rem; line-height:1.1; font-weight:800; letter-spacing:-.06em; margin:.6rem 0 .35rem; overflow-wrap:anywhere; }
.metric-note { color:var(--muted); font-size:.78rem; line-height:1.35; }
.section-head { display:flex; align-items:flex-end; justify-content:space-between; gap:1rem; margin:2.1rem 0 .8rem; border-bottom:1px solid var(--line); padding-bottom:.7rem; }
.section-head h2 { margin:0 !important; }.section-head span { color:var(--muted); font-size:.78rem; text-align:right; }
.insight { background:#e8f1e9; border:1px solid #c6d7c7; border-radius:12px; padding:.9rem 1rem; margin-bottom:.65rem; }
.insight strong { display:block; color:#1f5239; font-size:.87rem; margin-bottom:.18rem; }.insight p { color:#496256; margin:0; font-size:.78rem; line-height:1.5; }
[data-testid='stDataFrame'] { border:1px solid var(--line); border-radius:12px; overflow:hidden; background:var(--panel); max-width:100%; }
[data-testid='stDataFrame'] * { color:var(--ink) !important; }
[data-testid='stDataFrame'] [role='columnheader'] { background:#edf1eb !important; font-family:'DM Mono',monospace; font-size:.7rem; }
[data-testid='stDataFrame'] [role='gridcell'] { background:var(--panel) !important; }
[data-testid='stVegaLiteChart'] { background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:.7rem; overflow:hidden; max-width:100%; }
[data-testid='stAlert'] { background:#edf3ed; border:1px solid #c6d7c7; border-radius:12px; color:#234a36; }
button, [role='button'] { border-radius:9px !important; } button:focus-visible, [role='radio']:focus-visible { outline:2px solid #7cb092 !important; outline-offset:2px; }
@media (max-width: 760px) {
  html, body, .stApp, [data-testid='stAppViewContainer'], [data-testid='stMain'] { overflow-x:hidden !important; }
  .block-container { width:100%; max-width:100%; padding:1.55rem 1rem 2.5rem; }
  [data-testid='stHorizontalBlock'] { flex-direction:column !important; gap:1rem !important; }
  [data-testid='stHorizontalBlock'] > div { width:100% !important; min-width:0 !important; flex:1 1 auto !important; }
  h1 { font-size:2.2rem !important; } .section-head { align-items:flex-start; flex-direction:column; } .section-head span { text-align:left; } [data-testid='stDataFrame'] { font-size:.78rem; }
}
</style>""", unsafe_allow_html=True)


def hero(eyebrow: str, title: str, lede: str, badges: list[str]) -> None:
    badges_html = "".join(f"<span class='badge'>{badge}</span>" for badge in badges)
    st.markdown(
        f"<section class='hero'><div class='eyebrow'>{eyebrow}</div><h1>{title}</h1><p class='lede'>{lede}</p><div class='badge-row'>{badges_html}</div></section>",
        unsafe_allow_html=True,
    )


def section(title: str, note: str) -> None:
    st.markdown(f"<div class='section-head'><h2>{title}</h2><span>{note}</span></div>", unsafe_allow_html=True)


def metric(column, label: str, value: str | int, note: str) -> None:
    column.markdown(f"<div class='metric-card'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div><div class='metric-note'>{note}</div></div>", unsafe_allow_html=True)


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


if ensure_database(SAMPLE, DATABASE):
    st.cache_data.clear()

with st.sidebar:
    st.markdown("<div class='eyebrow' style='color:#a8d4b6;margin-top:.8rem'>Market intelligence</div>", unsafe_allow_html=True)
    st.title("SkillAtlas")
    st.caption("Observed job-market requirements. No hiring predictions.")
    st.divider()
    page = st.radio("Explore", ["Overview", "Roles", "Clusters", "Skill Gap", "Methods"])
    st.markdown("<div class='eyebrow' style='color:#a8d4b6;margin-top:1.3rem'>Filter evidence</div>", unsafe_allow_html=True)
    role = st.selectbox("Role filter", ROLES)
    location = st.selectbox("Location", ["All locations", *locations()])
    st.caption("Sample snapshot · 2026-02-14")

jobs = filtered_jobs(role, location)

if page == "Overview":
    skills = role_skill_summary(DATABASE, None if role == "All roles" else role)
    roles = role_summary(DATABASE)
    hero("Job-board analytics", "Data roles, decoded.", "A clean view of the tools and skills employers explicitly describe across selected data, AI, business, and software roles.", ["Source: bundled public sample", "Snapshot: 14 Feb 2026", f"Filter: {role}"])
    a, b, c = st.columns(3)
    metric(a, "Matched postings", len(jobs), "Unique cleaned postings in the current view")
    metric(b, "Roles covered", len(roles), "Ambiguous titles can appear in multiple roles")
    metric(c, "Top observed skill", skills.iloc[0].skill if not skills.empty else "—", "Most frequently matched skill in this filter")
    left, right = st.columns([1.35, .85], gap="large")
    with left:
        section("Skill demand", "Top 12 observed skills")
        st.bar_chart(skills.head(12).set_index("skill"), color="#207451")
        st.dataframe(skills.head(12), hide_index=True, use_container_width=True)
    with right:
        section("Readout", "Evidence, not recommendations")
        top_role = roles.iloc[0].role if not roles.empty else "—"
        st.markdown(f"<div class='insight'><strong>{top_role} leads this sample</strong><p>Role volume reflects matched job titles, not total openings in the market.</p></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='insight'><strong>{skills.iloc[0].skill if not skills.empty else 'No skill'} is most visible</strong><p>Skill counts show how often each dictionary match appears in a posting.</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='insight'><strong>Use the role filter to narrow evidence</strong><p>Every dashboard table and chart updates from the same SQLite analysis layer.</p></div>", unsafe_allow_html=True)
    section("Role comparison", "Multi-label counts shown transparently")
    st.dataframe(roles, hide_index=True, use_container_width=True)
    section("Recent evidence", "Latest rows in the selected filter")
    st.dataframe(jobs[["title", "company", "location", "posted_at"]].head(6), hide_index=True, use_container_width=True)

elif page == "Roles":
    selected = role if role != "All roles" else st.selectbox("Select a role", ROLES[1:])
    skills = role_skill_summary(DATABASE, selected)
    hero("Role evidence", selected, "Compare the skills surfaced from matched job descriptions. Values are posting counts, not importance scores.", [f"Role: {selected}", "Dictionary-backed extraction", "SQLite aggregate"])
    section("Observed skill mix", "Top 15 skills")
    st.bar_chart(skills.head(15).set_index("skill"), color="#207451")
    section("Skill table", "One count per posting")
    st.dataframe(skills, hide_index=True, use_container_width=True)

elif page == "Clusters":
    hero("Exploratory analysis", "Job clusters", "Clusters summarize overlaps in extracted skills. They are a lightweight exploration aid, not fixed job categories.", ["KMeans", "Fixed seed: 42", "Interpret with caution"])
    try:
        clusters = query(DATABASE, "select cluster, cluster_label, count(*) as posting_count from job_clusters group by cluster, cluster_label order by posting_count desc")
    except Exception:
        clusters = None
    if clusters is None or clusters.empty:
        st.info("This dataset is too small or homogeneous for a useful cluster. Role and skill evidence remains available.")
    else:
        section("Cluster composition", "Labels use common observed skills")
        st.bar_chart(clusters.set_index("cluster_label")[["posting_count"]], color="#207451")
        st.dataframe(clusters, hide_index=True, use_container_width=True)

elif page == "Skill Gap":
    hero("Personal evidence view", "Skill gap explorer", "Compare your entered skills with frequently observed skills for a selected role. This is a descriptive coverage view, not career advice.", ["Rule-based", "No profile stored", "Observed frequency"])
    target = st.selectbox("Target role", ROLES[1:])
    entered = st.text_input("Your skills", placeholder="Python, SQL, Docker")
    if entered:
        result = skill_gap(entered.split(","), role_skill_summary(DATABASE, target).head(12))
        a, b = st.columns([.7, 1.3], gap="large")
        metric(a, "Observed coverage", f"{result['coverage_percent']:.1f}%", f"Against displayed {target} skills")
        with b:
            st.markdown("<div class='insight'><strong>Matched</strong><p>" + (", ".join(result["matched"]) or "No recognized skills from this role’s observed list.") + "</p></div>", unsafe_allow_html=True)
            st.markdown("<div class='insight'><strong>Missing to explore</strong><p>" + (", ".join(result["missing"]) or "You cover the displayed skills.") + "</p></div>", unsafe_allow_html=True)
    else:
        st.info("Enter comma-separated skills to produce a transparent comparison.")

else:
    hero("Methodology", "How the evidence is built", "Every visual is derived from a small, reproducible batch pipeline. The app does not scrape live job boards or send portfolio inputs to a server.", ["Public sample", "Regex dictionary", "Local SQLite"])
    section("Method notes", "Visible assumptions")
    st.markdown("""- **Source:** bundled original sample data for a no-auth demo; larger public sources must be downloaded separately and documented before ingestion.
- **Roles:** transparent title rules; ambiguous titles may map to multiple roles.
- **Skills:** a regex dictionary with aliases such as PostgreSQL → SQL.
- **Clusters:** deterministic KMeans (`random_state=42`) on extracted-skill presence; weak results remain exploratory.
- **Privacy:** this app sends no data to external services.
""")
