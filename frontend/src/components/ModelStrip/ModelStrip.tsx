"use client";

import { useMemo } from "react";
import { useTimelineStore } from "@/stores/timeline-store";
import { useTimeline } from "@/hooks/useTimeline";
import ModelThumbnail from "./ModelThumbnail";

export default function ModelStrip() {
  const models = useTimelineStore((s) => s.models);
  const currentDate = useTimelineStore((s) => s.currentDate);
  const productType = useTimelineStore((s) => s.productType);
  const { jumpToYear } = useTimeline();

  const year = currentDate.getFullYear();

  const filteredModels = useMemo(() => {
    if (productType === "all") return models;
    return models.filter((m) => m.product_type === productType);
  }, [models, productType]);

  return (
    <section className="model-strip">
      <div className="model-strip-scroll">
        <div className="model-thumbnails">
          {filteredModels.map((model) => (
            <ModelThumbnail
              key={model.id}
              model={model}
              currentYear={year}
              onJumpToYear={jumpToYear}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
