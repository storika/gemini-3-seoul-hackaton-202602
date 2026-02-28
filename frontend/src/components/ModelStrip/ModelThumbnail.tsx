"use client";

import { useMemo, useState } from "react";
import { BRAND_LABELS } from "@/lib/constants";
import type { ModelEntry } from "@/lib/types";

const MIN_YEAR = 1924;
const MAX_YEAR = 2026;

const BRAND_BORDERS: Record<string, string> = {
  chamisul: "#2E7D32",
  chum_churum: "#1565C0",
  saero: "#F57C00",
  jinro_is_back: "#388E3C",
  jinro: "#1B5E20",
  goodday: "#AB47BC",
  san: "#6D4C41",
  green: "#66BB6A",
  ipseju: "#EF6C00",
  daesun: "#D84315",
  terra: "#00897B",
  terra_light: "#26A69A",
  cass: "#1565C0",
  cass_light: "#42A5F5",
  kloud: "#6A1B9A",
  kloud_draft: "#8E24AA",
  kloud_na: "#AB47BC",
  krush: "#D81B60",
  kelly: "#C62828",
  hite: "#0D47A1",
  max: "#BF360C",
  ob: "#1A237E",
  crown: "#4E342E",
  sunhari: "#F48FB1",
  isul_ttokttok: "#80DEEA",
};

interface Props {
  model: ModelEntry;
  currentYear: number;
  onJumpToYear: (year: number) => void;
}

export default function ModelThumbnail({ model, currentYear, onJumpToYear }: Props) {
  const [imgError, setImgError] = useState(false);

  const state = useMemo(() => {
    if (currentYear >= model.start_year && currentYear <= model.end_year) return "active";
    if (currentYear > model.end_year) return "past";
    return "future";
  }, [currentYear, model.start_year, model.end_year]);

  const pct = ((model.start_year - MIN_YEAR) / (MAX_YEAR - MIN_YEAR)) * 100;
  const durationPct = ((model.end_year - model.start_year) / (MAX_YEAR - MIN_YEAR)) * 100;
  const borderColor = BRAND_BORDERS[model.brand] || "#666";

  return (
    <div
      className={`model-thumb ${state}`}
      style={{ left: `${pct}%`, borderColor }}
      onClick={() => onJumpToYear(model.start_year)}
    >
      {!imgError ? (
        <img
          src={model.image_url}
          alt={model.name_ko}
          onError={() => setImgError(true)}
        />
      ) : (
        <span className="model-initials">{model.name_ko.charAt(0)}</span>
      )}

      <div className="model-tooltip">
        <strong>{model.name_ko}</strong>
        {model.company_ko && (
          <span className="model-tooltip-company">{model.company_ko}</span>
        )}
        <span className="model-tooltip-brand">
          {BRAND_LABELS[model.brand] || model.brand}
        </span>
        <span className="model-tooltip-years">
          {model.start_year}&ndash;{model.end_year}
        </span>
        {model.era_note && (
          <span className="model-tooltip-note">{model.era_note}</span>
        )}
      </div>

      <div
        className="model-duration-bar"
        style={{
          width: `${Math.max(durationPct, 0.5)}%`,
          backgroundColor: borderColor,
        }}
      />
    </div>
  );
}
