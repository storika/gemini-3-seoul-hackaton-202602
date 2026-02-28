import useSWR from "swr";
import { fetchEvents, fetchModels } from "@/lib/api";
import { useTimelineStore } from "@/stores/timeline-store";
import { useEffect } from "react";

async function fetchAll(industry: string) {
  const [events, models] = await Promise.all([fetchEvents(industry), fetchModels(industry)]);
  return { events, models };
}

export function useTimelineData() {
  const setEvents = useTimelineStore((s) => s.setEvents);
  const setModels = useTimelineStore((s) => s.setModels);
  const industry = useTimelineStore((s) => s.industry);

  const { data, error } = useSWR(["timeline-all", industry], () => fetchAll(industry), {
    revalidateOnFocus: false,
  });

  useEffect(() => {
    if (data) {
      setEvents(data.events);
      setModels(data.models);
    }
  }, [data, setEvents, setModels]);

  return {
    events: data?.events ?? [],
    models: data?.models ?? [],
    isLoading: !data && !error,
    error,
  };
}
