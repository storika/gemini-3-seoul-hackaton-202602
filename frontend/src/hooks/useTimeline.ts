import { useCallback, useRef } from "react";
import { useTimelineStore } from "@/stores/timeline-store";
import { MIN_DATE, MAX_DATE, TOTAL_MS, PLAY_INTERVAL_MS, PLAY_STEP_DAYS } from "@/lib/constants";

export function sliderToDate(val: number): Date {
  const ratio = val / 1000;
  const ms = MIN_DATE.getTime() + ratio * TOTAL_MS;
  return new Date(ms);
}

export function dateToSlider(date: Date): number {
  const ratio = (date.getTime() - MIN_DATE.getTime()) / TOTAL_MS;
  return Math.round(ratio * 1000);
}

export function useTimeline() {
  const setCurrentDate = useTimelineStore((s) => s.setCurrentDate);
  const isPlaying = useTimelineStore((s) => s.isPlaying);
  const setIsPlaying = useTimelineStore((s) => s.setIsPlaying);
  const playTimer = useRef<ReturnType<typeof setInterval> | null>(null);
  const sliderRef = useRef<HTMLInputElement | null>(null);

  const handleSliderChange = useCallback(
    (val: number) => {
      const date = sliderToDate(val);
      setCurrentDate(date);
    },
    [setCurrentDate]
  );

  const startPlay = useCallback(() => {
    setIsPlaying(true);
    playTimer.current = setInterval(() => {
      const slider = sliderRef.current;
      if (!slider) return;
      const current = sliderToDate(parseInt(slider.value));
      const next = new Date(current.getTime() + PLAY_STEP_DAYS * 86400000);
      if (next >= MAX_DATE) {
        if (playTimer.current) clearInterval(playTimer.current);
        setIsPlaying(false);
        return;
      }
      const newVal = dateToSlider(next);
      slider.value = String(newVal);
      setCurrentDate(next);
    }, PLAY_INTERVAL_MS);
  }, [setCurrentDate, setIsPlaying]);

  const stopPlay = useCallback(() => {
    setIsPlaying(false);
    if (playTimer.current) {
      clearInterval(playTimer.current);
      playTimer.current = null;
    }
  }, [setIsPlaying]);

  const togglePlay = useCallback(() => {
    if (isPlaying) stopPlay();
    else startPlay();
  }, [isPlaying, startPlay, stopPlay]);

  const resetTimeline = useCallback(() => {
    stopPlay();
    if (sliderRef.current) sliderRef.current.value = "0";
    setCurrentDate(MIN_DATE);
  }, [stopPlay, setCurrentDate]);

  const jumpToYear = useCallback(
    (year: number) => {
      const date = new Date(year, 0, 15);
      if (sliderRef.current) sliderRef.current.value = String(dateToSlider(date));
      setCurrentDate(date);
    },
    [setCurrentDate]
  );

  return {
    sliderRef,
    handleSliderChange,
    togglePlay,
    resetTimeline,
    jumpToYear,
    stopPlay,
  };
}
