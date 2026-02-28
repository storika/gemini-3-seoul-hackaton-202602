"use client";

import { useTimelineStore } from "@/stores/timeline-store";

const PRODUCT_TYPES = [
  { key: "all", label: "ALL" },
  { key: "soju", label: "SOJU" },
  { key: "beer", label: "BEER" },
];

const BRANDS = [
  { key: "all", label: "ALL" },
  { key: "jinro", label: "JINRO" },
  { key: "chamisul", label: "CHAMISUL" },
  { key: "chum_churum", label: "CHUM CHURUM" },
  { key: "saero", label: "SAERO" },
];

export default function Header() {
  const currentDate = useTimelineStore((s) => s.currentDate);
  const brand = useTimelineStore((s) => s.brand);
  const productType = useTimelineStore((s) => s.productType);
  const setBrand = useTimelineStore((s) => s.setBrand);
  const setProductType = useTimelineStore((s) => s.setProductType);

  const y = currentDate.getFullYear();
  const m = currentDate.getMonth() + 1;

  return (
    <header className="app-header">
      <h1>Soju Wars: 100-Year Brand Evolution</h1>

      <nav className="type-tabs">
        {PRODUCT_TYPES.map((t) => (
          <button
            key={t.key}
            className={`type-tab${productType === t.key ? " active" : ""}`}
            data-type={t.key}
            onClick={() => setProductType(t.key)}
          >
            {t.label}
          </button>
        ))}
      </nav>

      <nav className="brand-tabs">
        {BRANDS.map((b) => (
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
