"use client";

import { useMemo, useState } from "react";
import { useTimelineStore } from "@/stores/timeline-store";
import MarketShareBars from "./MarketShareBars";
import VideoPlayer from "./VideoPlayer";
import NewsSection from "./NewsSection";
import ActiveModelCards from "./ActiveModelCards";
import type { TimelineEvent } from "@/lib/types";

export default function DetailPanel() {
  const snapshot = useTimelineStore((s) => s.snapshot);
  const events = useTimelineStore((s) => s.events);
  const currentDate = useTimelineStore((s) => s.currentDate);
  const brand = useTimelineStore((s) => s.brand);
  const [heroImgLoaded, setHeroImgLoaded] = useState(false);

  // Find closest event to current date
  const currentEvent = useMemo<TimelineEvent | null>(() => {
    if (snapshot?.current_event) return snapshot.current_event;
    const filtered =
      brand === "all"
        ? events
        : events.filter((e) => e.brand === brand || e.brand === "multi");
    let closest: TimelineEvent | null = null;
    for (const evt of filtered) {
      if (new Date(evt.date) <= currentDate) closest = evt;
    }
    return closest;
  }, [snapshot, events, currentDate, brand]);

  if (!currentEvent) {
    return (
      <section className="detail-panel">
        <div className="detail-content">
          <div className="detail-placeholder">
            <p>
              타임라인을 스크롤하여
              <br />
              소주 브랜드 100년 역사를 탐색하세요
            </p>
          </div>
        </div>
      </section>
    );
  }

  const d = new Date(currentEvent.date);
  const dateStr = `${d.getFullYear()}. ${d.getMonth() + 1}. ${d.getDate()}.`;

  return (
    <section className="detail-panel">
      <div className="detail-content">
        <span className={`category-badge ${currentEvent.category}`}>
          {currentEvent.category.replace(/_/g, " ")}
        </span>
        <h2 className="detail-title">{currentEvent.title}</h2>
        <p className="title-ko">{currentEvent.title_ko}</p>
        <time className="detail-date">{dateStr}</time>

        <ActiveModelCards />

        {/* Hero Image */}
        {heroImgLoaded && (
          <div className="image-container">
            <img src={`/images/${currentEvent.id}/hero.png`} alt="Hero visual" />
          </div>
        )}
        <img
          src={`/images/${currentEvent.id}/hero.png`}
          alt=""
          style={{ display: "none" }}
          onLoad={() => setHeroImgLoaded(true)}
          onError={() => setHeroImgLoaded(false)}
        />

        <VideoPlayer event={currentEvent} />

        <NewsSection
          headlines={currentEvent.news_headlines}
          eventId={currentEvent.id}
        />

        <MarketShareBars
          marketShare={currentEvent.market_share}
          marketSales={currentEvent.market_sales}
        />

        <div className="kg-changes">
          <h3>KG Changes</h3>
          <span className="kg-mutations">
            +{currentEvent.kg_mutation_count} mutations
          </span>
        </div>

        <p className="detail-description">{currentEvent.description}</p>
      </div>
    </section>
  );
}
