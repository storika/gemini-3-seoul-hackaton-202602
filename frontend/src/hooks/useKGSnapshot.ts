import useSWR from "swr";
import { fetchKGSnapshot } from "@/lib/api";
import { useTimelineStore } from "@/stores/timeline-store";
import { useEffect, useState, useRef } from "react";
import { DEBOUNCE_MS } from "@/lib/constants";

export function useKGSnapshot() {
  const currentDate = useTimelineStore((s) => s.currentDate);
  const brand = useTimelineStore((s) => s.brand);
  const folVisible = useTimelineStore((s) => s.folVisible);
  const setSnapshot = useTimelineStore((s) => s.setSnapshot);

  const isoDate = currentDate.toISOString().slice(0, 10);
  const key = `${isoDate}|${brand}|${folVisible}`;

  // Debounce: update the fetched key after a short delay
  const [debouncedKey, setDebouncedKey] = useState(key);
  const isFirst = useRef(true);

  useEffect(() => {
    // Skip debounce on first render for instant initial load
    if (isFirst.current) {
      isFirst.current = false;
      setDebouncedKey(key);
      return;
    }
    const t = setTimeout(() => setDebouncedKey(key), DEBOUNCE_MS);
    return () => clearTimeout(t);
  }, [key]);

  const [dIso, dBrand, dFol] = debouncedKey.split("|");
  const includeFol = dFol === "true";

  const { data, error } = useSWR(
    ["kg-snapshot", dIso, dBrand, includeFol],
    () => fetchKGSnapshot(dIso, dBrand, includeFol),
    {
      revalidateOnFocus: false,
      keepPreviousData: true,
    }
  );

  useEffect(() => {
    if (data) setSnapshot(data);
  }, [data, setSnapshot]);

  return { snapshot: data ?? null, error };
}
