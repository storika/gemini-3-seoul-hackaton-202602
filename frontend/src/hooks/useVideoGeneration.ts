import { useState, useCallback } from "react";
import { generateVideo, fetchVideoStatus } from "@/lib/api";
import type { VideoStatus } from "@/lib/types";

export function useVideoGeneration() {
  const [status, setStatus] = useState<VideoStatus | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  const checkCache = useCallback(async (eventId: string) => {
    const result = await fetchVideoStatus(eventId);
    setStatus(result);
    return result;
  }, []);

  const generate = useCallback(
    async (eventId: string, prompt: string) => {
      setIsGenerating(true);
      try {
        const result = await generateVideo(eventId, prompt);
        setStatus(result);
        return result;
      } finally {
        setIsGenerating(false);
      }
    },
    []
  );

  const reset = useCallback(() => {
    setStatus(null);
    setIsGenerating(false);
  }, []);

  return { status, isGenerating, checkCache, generate, reset };
}
