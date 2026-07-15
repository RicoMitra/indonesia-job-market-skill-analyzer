export type Skill = { skill: string; posting_count: number };
export type RoleCount = { role: string; posting_count: number };
export type EvidenceJob = { job_id: string; title: string; company: string; location: string; posted_at: string; roles: string };

export type DashboardData = {
  overview: {
    generated_at: string;
    source: { name: string; type: string; disclosure: string };
    kpis: { matched_postings: number; roles_covered: number; top_observed_skill: string | null };
    top_skills: Skill[];
    role_comparison: RoleCount[];
  };
  roleSkills: { generated_at: string; roles: Record<string, Skill[]> };
  clusters: { generated_at: string; exploratory: boolean; clusters: { id: number; label: string; posting_count: number; defining_skills: string[] }[] };
  evidence: { generated_at: string; jobs: EvidenceJob[] };
};
