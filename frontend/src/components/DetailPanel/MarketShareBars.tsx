"use client";

import { useEffect, useRef } from "react";

const BRAND_COLORS: Record<string, string> = {
  "\uC9C4\uB85C": "#1B5E20",
  "\uC9C4\uB85C(\uCC38\uC774\uC2AC)": "#2E7D32",
  "\uCC38\uC774\uC2AC": "#2E7D32",
  "\uCC98\uC74C\uCC98\uB7FC": "#1565C0",
  "\uC0C8\uB85C": "#F57C00",
  "\uC9C4\uB85C\uC774\uC988\uBC31": "#388E3C",
  "\uACBD\uC6D4\uC18C\uC8FC": "#5D4037",
  "\uBB34\uD559": "#616161",
};

interface Props {
  marketShare: Record<string, number>;
  marketSales?: Record<string, string>;
}

export default function MarketShareBars({ marketShare, marketSales }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Trigger animation after mount
    const fills = containerRef.current?.querySelectorAll<HTMLDivElement>(".share-bar-fill");
    if (fills) {
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          fills.forEach((fill) => {
            fill.style.width = fill.dataset.width || "0%";
          });
        });
      });
    }
  }, [marketShare]);

  if (!marketShare || Object.keys(marketShare).length === 0) return null;

  const sorted = Object.entries(marketShare).sort((a, b) => b[1] - a[1]);

  return (
    <div className="market-share-section">
      <h3>Market Share Rankings</h3>
      <div ref={containerRef}>
        {sorted.map(([brand, share], idx) => {
          const salesText = marketSales?.[brand] ? ` (${marketSales[brand]})` : "";
          const color = BRAND_COLORS[brand] || "#666";
          return (
            <div key={brand} className="share-bar-row">
              <span className={`share-rank${idx === 0 ? " rank-1" : ""}`}>
                {idx + 1}
              </span>
              <span className="share-brand-label">{brand}</span>
              <div className="share-bar-track">
                <div
                  className="share-bar-fill"
                  style={{ width: "0%", backgroundColor: color }}
                  data-width={`${Math.min(share * 1.5, 100)}%`}
                >
                  <span>
                    {share}%{salesText}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
