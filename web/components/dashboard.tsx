"use client";

import { useMemo, useState } from "react";

import { RoleBars, SkillBars } from "@/components/charts";
import type { DashboardData, EvidenceJob, Skill } from "@/lib/types";

type View = "Overview" | "Roles" | "Clusters" | "Skill Gap" | "Methods";
const views: View[] = ["Overview", "Roles", "Clusters", "Skill Gap", "Methods"];

function PanelTitle({ eyebrow, title, note }: { eyebrow: string; title: string; note?: string }) {
  return <header className="panel-title"><p className="eyebrow">{eyebrow}</p><h2>{title}</h2>{note && <p className="section-note">{note}</p>}</header>;
}

function EmptyState({ children }: { children: React.ReactNode }) {
  return <div className="empty-state">{children}</div>;
}

function EvidenceTable({ jobs, role }: { jobs: EvidenceJob[]; role?: string }) {
  const filtered = role ? jobs.filter((job) => job.roles.split(" | ").includes(role)) : jobs;
  return <div className="table-shell"><table><thead><tr><th>Posting</th><th>Company</th><th>Location</th><th>Matched role</th></tr></thead><tbody>
    {filtered.slice(0, 8).map((job) => <tr key={job.job_id}><td><strong>{job.title}</strong><span>{job.posted_at || "Undated sample"}</span></td><td>{job.company || "Not disclosed"}</td><td>{job.location || "Not disclosed"}</td><td><span className="role-chip">{job.roles}</span></td></tr>)}
  </tbody></table></div>;
}

export function Dashboard({ data }: { data: DashboardData }) {
  const [view, setView] = useState<View>("Overview");
  const [selectedRole, setSelectedRole] = useState(Object.keys(data.roleSkills.roles)[0] ?? "");
  const [skillsInput, setSkillsInput] = useState("");
  const selectedSkills = data.roleSkills.roles[selectedRole] ?? [];
  const entered = useMemo(() => new Set(skillsInput.split(",").map((skill) => skill.trim().toLowerCase()).filter(Boolean)), [skillsInput]);
  const matched = selectedSkills.filter((skill) => entered.has(skill.skill.toLowerCase()));
  const missing = selectedSkills.filter((skill) => !entered.has(skill.skill.toLowerCase()));
  const coverage = selectedSkills.length ? Math.round((matched.length / selectedSkills.length) * 100) : 0;
  const snapshot = new Intl.DateTimeFormat("en", { year: "numeric", month: "short", day: "2-digit" }).format(new Date(data.overview.generated_at));

  return <div className="app-shell">
    <aside className="sidebar"><div className="brand"><span className="brand-mark">S</span><div><strong>SkillAtlas</strong><span>MARKET EVIDENCE</span></div></div>
      <p className="sidebar-kicker">INDONESIA / SKILLS INTELLIGENCE</p>
      <nav aria-label="Dashboard sections">{views.map((item, index) => <button key={item} className={view === item ? "nav-item active" : "nav-item"} onClick={() => setView(item)}><span>{String(index + 1).padStart(2, "0")}</span>{item}</button>)}</nav>
      <div className="sidebar-footer"><span className="status-dot" />Static pipeline artifact<br /><small>Snapshot {snapshot}</small></div>
    </aside>
    <main className="main-content">
      <header className="topbar"><div><p className="eyebrow">REPRODUCIBLE JOB-MARKET ANALYSIS</p><h1>{view}</h1></div><div className="source-badge"><span>DATA STATUS</span><strong>STATIC / VERIFIED</strong></div></header>
      {view === "Overview" && <Overview data={data} snapshot={snapshot} />}
      {view === "Roles" && <Roles data={data} selectedRole={selectedRole} onRoleChange={setSelectedRole} />}
      {view === "Clusters" && <Clusters data={data} />}
      {view === "Skill Gap" && <SkillGap selectedRole={selectedRole} onRoleChange={setSelectedRole} allRoles={Object.keys(data.roleSkills.roles)} entered={skillsInput} onEnteredChange={setSkillsInput} matched={matched} missing={missing} coverage={coverage} />}
      {view === "Methods" && <Methods data={data} />}
    </main>
  </div>;
}

function Overview({ data, snapshot }: { data: DashboardData; snapshot: string }) {
  const kpis = data.overview.kpis;
  return <>
    <section className="intro-grid"><div><p className="lede">A bounded evidence layer for tools and skills explicitly observed in Indonesian data, AI, business, and software postings.</p><div className="metadata-row"><span>Source: {data.overview.source.name}</span><span>Generated: {snapshot}</span></div></div><div className="disclosure"><strong>Source disclosure</strong><p>{data.overview.source.disclosure}</p></div></section>
    <section className="kpi-grid" aria-label="Overview metrics"><Metric label="Matched postings" value={kpis.matched_postings} note="Cleaned, role-mapped records" /><Metric label="Roles covered" value={kpis.roles_covered} note="Multi-label title mapping" /><Metric label="Top observed skill" value={kpis.top_observed_skill ?? "—"} note="Dictionary-matched frequency" /></section>
    <section className="content-grid overview-grid"><article className="data-panel wide"><PanelTitle eyebrow="SKILL DEMAND" title="Most visible requirements" note="Unique postings containing each dictionary match" /><SkillBars data={data.overview.top_skills} /></article><article className="data-panel"><PanelTitle eyebrow="READOUT" title="Interpretation" /><div className="insight-stack"><Insight label="Evidence, not scoring" text="Counts represent mentions across the sample; they do not rank skills by employer importance." /><Insight label="Role counts can overlap" text="One title can map to multiple roles when the title explicitly signals ambiguity." /><Insight label="Traceable from source" text="The same Python pipeline creates every visible number and table." /></div></article></section>
    <section className="content-grid overview-grid"><article className="data-panel"><PanelTitle eyebrow="ROLE COMPARISON" title="Matched volume by role" note="Transparent multi-label counts" /><RoleBars data={data.overview.role_comparison} /></article><article className="data-panel"><PanelTitle eyebrow="EVIDENCE ROWS" title="Recent sample postings" note="Raw posting fields retained after cleaning" /><EvidenceTable jobs={data.evidence.jobs} /></article></section>
  </>;
}

function Metric({ label, value, note }: { label: string; value: string | number; note: string }) { return <article className="metric"><p>{label}</p><strong>{value}</strong><span>{note}</span></article>; }
function Insight({ label, text }: { label: string; text: string }) { return <div className="insight"><strong>{label}</strong><p>{text}</p></div>; }

function Roles({ data, selectedRole, onRoleChange }: { data: DashboardData; selectedRole: string; onRoleChange: (role: string) => void }) { return <>
  <section className="intro-grid compact"><div><p className="lede">Select a mapped role to inspect the Python-generated skill-frequency summary and the evidence rows behind it.</p></div><label className="select-field"><span>Role selector</span><select value={selectedRole} onChange={(event) => onRoleChange(event.target.value)}>{Object.keys(data.roleSkills.roles).map((role) => <option key={role}>{role}</option>)}</select></label></section>
  <section className="content-grid role-grid"><article className="data-panel wide"><PanelTitle eyebrow="OBSERVED SKILL MIX" title={selectedRole} note="Posting count per extracted skill" /><SkillBars data={data.roleSkills.roles[selectedRole] ?? []} limit={15} /></article><article className="data-panel"><PanelTitle eyebrow="SKILL LEDGER" title="Frequency table" /><SkillLedger data={data.roleSkills.roles[selectedRole] ?? []} /></article></section>
  <section className="data-panel"><PanelTitle eyebrow="EVIDENCE POSTINGS" title="Mapped sample rows" note="Job title, employer, location, and matching role" /><EvidenceTable jobs={data.evidence.jobs} role={selectedRole} /></section>
</>; }
function SkillLedger({ data }: { data: Skill[] }) { return <div className="skill-ledger">{data.map((item, index) => <div key={item.skill}><span>{String(index + 1).padStart(2, "0")}</span><strong>{item.skill}</strong><b>{item.posting_count}</b></div>)}</div>; }

function Clusters({ data }: { data: DashboardData }) { return <><section className="intro-grid"><div><p className="lede">A deliberately cautious read of co-occurring skill sets. Clustering is exploratory and does not create authoritative job categories.</p></div><div className="disclosure"><strong>Method status</strong><p>Deterministic KMeans on skill-presence vectors. Treat sample patterns as prompts for inspection.</p></div></section><section className="cluster-list">{data.clusters.clusters.map((cluster) => <article className="cluster-card" key={cluster.id}><div><p className="eyebrow">CLUSTER {String(cluster.id + 1).padStart(2, "0")}</p><h2>{cluster.label}</h2><span>{cluster.posting_count} matched postings</span></div><div className="cluster-skills">{cluster.defining_skills.map((skill) => <span key={skill}>{skill}</span>)}</div></article>)}</section></>; }

function SkillGap({ selectedRole, onRoleChange, allRoles, entered, onEnteredChange, matched, missing, coverage }: { selectedRole: string; onRoleChange: (role: string) => void; allRoles: string[]; entered: string; onEnteredChange: (value: string) => void; matched: Skill[]; missing: Skill[]; coverage: number }) { return <><section className="intro-grid compact"><div><p className="lede">Enter exact canonical skill names, separated by commas. This UI compares your input against the precomputed Python role summary; it does not infer skills or provide career advice.</p></div><label className="select-field"><span>Target role</span><select value={selectedRole} onChange={(event) => onRoleChange(event.target.value)}>{allRoles.map((role) => <option key={role}>{role}</option>)}</select></label></section><section className="gap-input"><label htmlFor="skills"><span>Your skills</span><input id="skills" value={entered} onChange={(event) => onEnteredChange(event.target.value)} placeholder="Python, SQL, Docker" /><small>Use the labels shown in the role ledger for exact matching.</small></label></section><section className="content-grid gap-grid"><article className="coverage-panel"><p className="eyebrow">OBSERVED COVERAGE</p><strong>{coverage}<small>%</small></strong><p>Share of displayed {selectedRole} skills present in your entered list.</p><div className="coverage-track"><i style={{ width: `${coverage}%` }} /></div></article><article className="data-panel"><PanelTitle eyebrow="MATCHED" title="Already in your list" /><SkillChips skills={matched} empty="No exact canonical skills matched yet." tone="good" /></article><article className="data-panel"><PanelTitle eyebrow="MISSING TO EXPLORE" title="Observed requirements" /><SkillChips skills={missing} empty="You cover every displayed skill." tone="neutral" /></article></section></>; }
function SkillChips({ skills, empty, tone }: { skills: Skill[]; empty: string; tone: "good" | "neutral" }) { return skills.length ? <div className={`skill-chips ${tone}`}>{skills.map(({ skill, posting_count }) => <span key={skill}>{skill}<b>{posting_count}</b></span>)}</div> : <EmptyState>{empty}</EmptyState>; }

function Methods({ data }: { data: DashboardData }) { return <section className="methods"><div className="method-head"><p className="eyebrow">METHODS / LIMITATIONS</p><h2>Designed for inspection, not prediction.</h2><p>The frontend is a read-only presentation layer for versioned JSON artifacts from the Python pipeline.</p></div><div className="method-list"><Method number="01" title="Dataset" text={`${data.overview.source.name}. It is bundled for reproducibility and should not be represented as a live labor-market feed.`} /><Method number="02" title="Pipeline" text="Pandas cleaning, transparent title rules, regex skill extraction, SQLite aggregates, and exploratory KMeans run in Python." /><Method number="03" title="Role mapping" text="Titles map to six target roles. Explicitly ambiguous titles may map to more than one role." /><Method number="04" title="Skill dictionary" text="Canonical skills and aliases live in the Python dictionary. The web app does not run NLP or extraction." /><Method number="05" title="Limitations" text="Small sample sizes, dictionary coverage, and weak cluster quality limit generalization. Counts are observed mentions, not demand forecasts." /></div></section>; }
function Method({ number, title, text }: { number: string; title: string; text: string }) { return <article><span>{number}</span><div><h3>{title}</h3><p>{text}</p></div></article>; }
