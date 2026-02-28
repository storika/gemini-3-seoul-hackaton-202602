"use client";

import { useMemo } from "react";
import { useTimelineStore } from "@/stores/timeline-store";
import { BRAND_LABELS } from "@/lib/constants";

const BRAND_BORDERS: Record<string, string> = {
  chamisul: "#2E7D32",
  chum_churum: "#1565C0",
  saero: "#F57C00",
  jinro_is_back: "#388E3C",
  jinro: "#1B5E20",
  goodday: "#AB47BC",
  terra: "#00897B",
  cass: "#1565C0",
  kloud: "#6A1B9A",
  krush: "#D81B60",
  kelly: "#C62828",
  hite: "#0D47A1",
};

export default function ActiveModelCards() {
  const currentDate = useTimelineStore((s) => s.currentDate);
  const models = useTimelineStore((s) => s.models);
  const productType = useTimelineStore((s) => s.productType);

  const year = currentDate.getFullYear();

  const activeModels = useMemo(() => {
    const filtered =
      productType === "all"
        ? models
        : models.filter((m) => m.product_type === productType);
    return filtered.filter((m) => year >= m.start_year && year <= m.end_year);
  }, [models, year, productType]);

  if (activeModels.length === 0) return null;

  return (
    <div className="active-model-section">
      <div className="active-model-cards">
        {activeModels.map((model) => {
          const borderColor = BRAND_BORDERS[model.brand] || "#666";
          return (
            <div key={model.id} className={`active-model-card brand-${model.brand}`}>
              <div className="active-model-img-wrap" style={{ borderColor }}>
                <img
                  src={model.image_url}
                  alt={model.name_ko}
                  onError={(e) => {
                    const parent = (e.target as HTMLImageElement).parentElement;
                    if (parent) parent.innerHTML = `<span>${model.name_ko.charAt(0)}</span>`;
                  }}
                />
              </div>
              <div className="active-model-info">
                <strong>{model.name_ko}</strong>
                {model.company_ko && (
                  <span className="active-model-company">{model.company_ko}</span>
                )}
                <span className="active-model-brand" style={{ color: borderColor }}>
                  {BRAND_LABELS[model.brand] || model.brand}
                </span>
                <span className="active-model-years">
                  {model.start_year}&ndash;{model.end_year}
                </span>
                {model.era_note && (
                  <p className="active-model-note">{model.era_note}</p>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
