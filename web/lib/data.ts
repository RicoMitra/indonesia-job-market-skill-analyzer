import { readFile } from "node:fs/promises";
import { join } from "node:path";

import type { DashboardData } from "@/lib/types";

async function readJson<T>(name: string): Promise<T> {
  const file = await readFile(join(process.cwd(), "public", "data", name), "utf8");
  return JSON.parse(file) as T;
}

export async function getDashboardData(): Promise<DashboardData> {
  const [overview, roleSkills, clusters, evidence] = await Promise.all([
    readJson<DashboardData["overview"]>("overview.json"),
    readJson<DashboardData["roleSkills"]>("role_skills.json"),
    readJson<DashboardData["clusters"]>("clusters.json"),
    readJson<DashboardData["evidence"]>("evidence_jobs.json"),
  ]);
  return { overview, roleSkills, clusters, evidence };
}
