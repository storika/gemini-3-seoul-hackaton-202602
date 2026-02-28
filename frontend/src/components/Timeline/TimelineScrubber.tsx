"use client";

import { useTimeline, dateToSlider } from "@/hooks/useTimeline";
import { useTimelineStore } from "@/stores/timeline-store";
import TimelineMarkers from "./TimelineMarkers";
import { useCallback } from "react";

export default function TimelineScrubber() {
  const isPlaying = useTimelineStore((s) => s.isPlaying);
  const { sliderRef, handleSliderChange, togglePlay, resetTimeline } =
    useTimeline();

  const onInput = useCallback(
    (e: React.FormEvent<HTMLInputElement>) => {
      handleSliderChange(parseInt((e.target as HTMLInputElement).value));
    },
    [handleSliderChange]
  );

  return (
    <footer className="timeline-footer">
      <div className="timeline-track">
        <span className="timeline-label">1924</span>
        <div className="timeline-slider-container">
          <input
            ref={sliderRef}
            type="range"
            className="timeline-slider"
            min={0}
            max={1000}
            defaultValue={0}
            step={1}
            onInput={onInput}
          />
          <TimelineMarkers />
        </div>
        <span className="timeline-label">2026</span>
      </div>
      <div className="timeline-controls">
        <button
          onClick={togglePlay}
          className={isPlaying ? "playing" : ""}
        >
          {isPlaying ? "⏸ Pause" : "▶ Play"}
        </button>
        <button onClick={resetTimeline}>↴ Reset</button>
      </div>
    </footer>
  );
}
