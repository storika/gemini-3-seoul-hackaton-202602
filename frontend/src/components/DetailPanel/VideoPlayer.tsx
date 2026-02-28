"use client";

import { useEffect, useState } from "react";
import { useVideoGeneration } from "@/hooks/useVideoGeneration";
import type { TimelineEvent } from "@/lib/types";

interface Props {
  event: TimelineEvent | null;
}

export default function VideoPlayer({ event }: Props) {
  const { status, isGenerating, checkCache, generate, reset } = useVideoGeneration();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    reset();
    setError(null);
    if (event) checkCache(event.id);
  }, [event?.id]);

  const handleGenerate = async () => {
    if (!event) return;
    setError(null);
    const result = await generate(event.id, event.video_prompt);
    if (result.status === "error") {
      setError(result.detail || "Generation failed");
    }
  };

  const videoAvailable =
    status?.status === "available" ||
    status?.status === "generated" ||
    status?.status === "cached";

  if (!videoAvailable || !status?.path) return null;

  return (
    <div className="video-container">
      <video className="event-video" controls src={status.path} />
    </div>
  );
}
