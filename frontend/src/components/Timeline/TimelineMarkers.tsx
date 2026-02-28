"use client";

import { useTimelineStore } from "@/stores/timeline-store";
import { MIN_DATE, TOTAL_MS } from "@/lib/constants";

export default function TimelineMarkers() {
  const events = useTimelineStore((s) => s.events);
  const currentDate = useTimelineStore((s) => s.currentDate);

  return (
    <div className="timeline-markers">
      {events.map((evt) => {
        const d = new Date(evt.date);
        const pct = ((d.getTime() - MIN_DATE.getTime()) / TOTAL_MS) * 100;
        const active = d <= currentDate;
        return (
          <div
            key={evt.id}
            className={`timeline-marker brand-${evt.brand}${active ? " active" : ""}`}
            style={{ left: `${pct}%` }}
            title={`${evt.title_ko || evt.title} (${evt.date.slice(0, 7)})`}
          />
        );
      })}
    </div>
  );
}
