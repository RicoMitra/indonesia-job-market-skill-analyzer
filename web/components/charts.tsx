"use client";

import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { RoleCount, Skill } from "@/lib/types";

const GREEN = "#235c42";
const PALE = "#95ae9c";

function TooltipPanel({ active, payload }: { active?: boolean; payload?: { value?: number; payload?: { skill?: string; role?: string } }[] }) {
  if (!active || !payload?.length) return null;
  const item = payload[0];
  return <div className="chart-tooltip"><span>{item.payload?.skill ?? item.payload?.role}</span><strong>{item.value} postings</strong></div>;
}

export function SkillBars({ data, limit = 12 }: { data: Skill[]; limit?: number }) {
  const display = data.slice(0, limit);
  return <div className="chart-wrap" role="img" aria-label="Bar chart showing observed skill frequency">
    <ResponsiveContainer width="100%" height={Math.max(260, display.length * 31)}>
      <BarChart data={display} layout="vertical" margin={{ top: 4, right: 20, left: 4, bottom: 4 }}>
        <CartesianGrid horizontal={false} stroke="#d9ddd4" />
        <XAxis type="number" tickLine={false} axisLine={false} tick={{ fill: "#637066", fontSize: 11 }} allowDecimals={false} />
        <YAxis type="category" dataKey="skill" width={96} tickLine={false} axisLine={false} tick={{ fill: "#28342e", fontSize: 12 }} />
        <Tooltip content={<TooltipPanel />} cursor={{ fill: "#edf0e9" }} />
        <Bar dataKey="posting_count" fill={GREEN} radius={[0, 2, 2, 0]} maxBarSize={17} />
      </BarChart>
    </ResponsiveContainer>
  </div>;
}

export function RoleBars({ data }: { data: RoleCount[] }) {
  return <div className="chart-wrap short" role="img" aria-label="Bar chart showing matched postings per role">
    <ResponsiveContainer width="100%" height={245}>
      <BarChart data={data} margin={{ top: 8, right: 8, left: -18, bottom: 46 }}>
        <CartesianGrid vertical={false} stroke="#d9ddd4" />
        <XAxis dataKey="role" angle={-32} textAnchor="end" interval={0} tickLine={false} axisLine={false} tick={{ fill: "#637066", fontSize: 10 }} />
        <YAxis allowDecimals={false} tickLine={false} axisLine={false} tick={{ fill: "#637066", fontSize: 11 }} />
        <Tooltip content={<TooltipPanel />} cursor={{ fill: "#edf0e9" }} />
        <Bar dataKey="posting_count" radius={[2, 2, 0, 0]} maxBarSize={34}>
          {data.map((entry, index) => <Cell key={entry.role} fill={index === 0 ? GREEN : PALE} />)}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  </div>;
}
