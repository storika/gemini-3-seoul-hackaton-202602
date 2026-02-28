import useSWR from "swr";
import { fetchEvents, fetchModels } from "@/lib/api";
import { useTimelineStore } from "@/stores/timeline-store";
import { useEffect } from "react";

async function fetchAll() {
  const [events, models] = await Promise.all([fetchEvents(), fetchModels()]);
  return { events, models };
}

export function useTimelineData() {
  const setEvents = useTimelineStore((s) => s.setEvents);
  const setModels = useTimelineStore((s) => s.setModels);

  const { data, error } = useSWR("timeline-all", fetchAll, {
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
