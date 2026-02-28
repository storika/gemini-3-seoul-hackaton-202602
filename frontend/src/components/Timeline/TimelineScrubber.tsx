"use client";

import { useTimeline, dateToSlider } from "@/hooks/useTimeline";
import { useTimelineStore } from "@/stores/timeline-store";
import { fetchLiveRecommendation } from "@/lib/api";
import TimelineMarkers from "./TimelineMarkers";
import { useCallback } from "react";

export default function TimelineScrubber() {
  const isPlaying = useTimelineStore((s) => s.isPlaying);
  const liveMode = useTimelineStore((s) => s.liveMode);
  const industry = useTimelineStore((s) => s.industry);
  const brand = useTimelineStore((s) => s.brand);
  const setLiveMode = useTimelineStore((s) => s.setLiveMode);
  const setLiveRecommendation = useTimelineStore((s) => s.setLiveRecommendation);
  const toggleFOL = useTimelineStore((s) => s.toggleFOL);
  const folVisible = useTimelineStore((s) => s.folVisible);
  const { sliderRef, handleSliderChange, togglePlay, resetTimeline, stopPlay } =
    useTimeline();

  const onInput = useCallback(
    (e: React.FormEvent<HTMLInputElement>) => {
      handleSliderChange(parseInt((e.target as HTMLInputElement).value));
      // Slider movement disables LIVE mode
      if (liveMode) {
        setLiveMode(false);
        setLiveRecommendation(null);
      }
    },
    [handleSliderChange, liveMode, setLiveMode, setLiveRecommendation]
  );

  const activateLive = useCallback(async () => {
    // Stop playback
    stopPlay();
    // Jump slider to 2026-02-28
    const liveDate = new Date(2026, 1, 28);
    const sliderVal = dateToSlider(liveDate);
    if (sliderRef.current) sliderRef.current.value = String(sliderVal);
    handleSliderChange(sliderVal);
    // Enable FOL if not already
    if (!folVisible) toggleFOL();
    // Enable live mode
    setLiveMode(true);
    // Fetch recommendation
    try {
      const rec = await fetchLiveRecommendation(industry, brand);
      setLiveRecommendation(rec);
    } catch {
      setLiveRecommendation(null);
    }
  }, [stopPlay, sliderRef, handleSliderChange, folVisible, toggleFOL, setLiveMode, industry, brand, setLiveRecommendation]);

  const deactivateLive = useCallback(() => {
    setLiveMode(false);
    setLiveRecommendation(null);
  }, [setLiveMode, setLiveRecommendation]);

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
        <button
          className={`live-button${liveMode ? " live-active" : ""}`}
          onClick={liveMode ? deactivateLive : activateLive}
        >
          ● LIVE
        </button>
      </div>
    </footer>
  );
}
