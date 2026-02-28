"use client";

import { useTimelineStore } from "@/stores/timeline-store";

const INDUSTRY_TABS = [
  { key: "all", label: "ALL" },
  { key: "soju", label: "SOJU" },
  { key: "whisky", label: "WHISKY" },
];

const BRANDS_BY_INDUSTRY: Record<string, { key: string; label: string }[]> = {
  all: [
    { key: "all", label: "ALL" },
    { key: "jinro", label: "JINRO" },
    { key: "chamisul", label: "CHAMISUL" },
    { key: "chum_churum", label: "CHUM CHURUM" },
    { key: "saero", label: "SAERO" },
    { key: "jw_global", label: "JOHNNIE WALKER" },
  ],
  soju: [
    { key: "all", label: "ALL" },
    { key: "jinro", label: "JINRO" },
    { key: "chamisul", label: "CHAMISUL" },
    { key: "chum_churum", label: "CHUM CHURUM" },
    { key: "saero", label: "SAERO" },
  ],
  beer: [
    { key: "all", label: "ALL" },
  ],
  whisky: [
    { key: "all", label: "ALL" },
    { key: "jw_global", label: "JW GLOBAL" },
    { key: "jw_red", label: "RED LABEL" },
    { key: "jw_black", label: "BLACK LABEL" },
    { key: "jw_blue", label: "BLUE LABEL" },
  ],
};

export default function Header() {
  const currentDate = useTimelineStore((s) => s.currentDate);
  const brand = useTimelineStore((s) => s.brand);
  const industry = useTimelineStore((s) => s.industry);
  const setBrand = useTimelineStore((s) => s.setBrand);
  const setIndustry = useTimelineStore((s) => s.setIndustry);

  const y = currentDate.getFullYear();
  const m = currentDate.getMonth() + 1;

  const brands = BRANDS_BY_INDUSTRY[industry] ?? BRANDS_BY_INDUSTRY.all;

  const handleIndustryChange = (key: string) => {
    setIndustry(key);
    setBrand("all");
  };

  return (
    <header className="app-header">
      <h1>Brand Wars: 100-Year Evolution</h1>

      <nav className="type-tabs">
        {INDUSTRY_TABS.map((t) => (
          <button
            key={t.key}
            className={`type-tab${industry === t.key ? " active" : ""}`}
            data-type={t.key}
            onClick={() => handleIndustryChange(t.key)}
          >
            {t.label}
          </button>
        ))}
      </nav>

      <nav className="brand-tabs">
        {brands.map((b) => (
          <button
            key={b.key}
            className={`brand-tab${brand === b.key ? " active" : ""}`}
            data-brand={b.key}
            onClick={() => setBrand(b.key)}
          >
            {b.label}
          </button>
        ))}
      </nav>

      <div className="date-display">
        {y}년 {m}월
      </div>
    </header>
  );
}
