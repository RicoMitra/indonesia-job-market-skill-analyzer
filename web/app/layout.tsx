import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SkillAtlas | Indonesia Job Market Evidence",
  description: "A reproducible analysis of observed skills in Indonesian job descriptions.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
