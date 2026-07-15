import { Dashboard } from "@/components/dashboard";
import { getDashboardData } from "@/lib/data";

export default async function Home() {
  return <Dashboard data={await getDashboardData()} />;
}
