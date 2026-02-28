import type { TimelineEvent, KGSnapshot, ModelEntry, VideoStatus } from "./types";

export async function fetchEvents(industry?: string): Promise<TimelineEvent[]> {
  const params = new URLSearchParams();
  if (industry && industry !== "all") params.set("industry", industry);
  const qs = params.toString();
  const res = await fetch(`/api/timeline/events${qs ? `?${qs}` : ""}`);
  if (!res.ok) throw new Error("Failed to fetch events");
  return res.json();
}

export async function fetchModels(industry?: string): Promise<ModelEntry[]> {
  const params = new URLSearchParams();
  if (industry && industry !== "all") params.set("industry", industry);
  const qs = params.toString();
  const res = await fetch(`/api/timeline/models${qs ? `?${qs}` : ""}`);
  if (!res.ok) throw new Error("Failed to fetch models");
  return res.json();
}

export async function fetchKGSnapshot(
  date: string,
  brand: string = "all",
  includeFol: boolean = false,
  alpha?: number,
  industry: string = "all"
): Promise<KGSnapshot> {
  const params = new URLSearchParams({ date, brand });
  if (includeFol) params.set("include_fol", "true");
  if (alpha !== undefined) params.set("alpha", String(alpha));
  if (industry && industry !== "all") params.set("industry", industry);
  const res = await fetch(`/api/kg/snapshot?${params}`);
  if (!res.ok) throw new Error("Failed to fetch KG snapshot");
  return res.json();
}

export async function fetchVideoStatus(eventId: string): Promise<VideoStatus> {
  const res = await fetch(`/api/media/video/${eventId}`);
  if (!res.ok) return { status: "not_found" };
  return res.json();
}

export async function generateVideo(
  eventId: string,
  prompt: string,
  aspectRatio: string = "16:9",
  durationSeconds: number = 8
): Promise<VideoStatus> {
  const res = await fetch("/api/media/generate-video", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      event_id: eventId,
      prompt,
      aspect_ratio: aspectRatio,
      duration_seconds: durationSeconds,
    }),
  });
  if (!res.ok) return { status: "error", detail: "Request failed" };
  return res.json();
}
