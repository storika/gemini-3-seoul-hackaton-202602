import { create } from "zustand";
import type { TimelineEvent, KGSnapshot, ModelEntry } from "@/lib/types";

interface TimelineState {
  currentDate: Date;
  brand: string;
  productType: string;
  industry: string;
  events: TimelineEvent[];
  models: ModelEntry[];
  snapshot: KGSnapshot | null;
  isPlaying: boolean;
  folVisible: boolean;
  selectedEventId: string | null;

  setCurrentDate: (date: Date) => void;
  setBrand: (brand: string) => void;
  setProductType: (type: string) => void;
  setIndustry: (industry: string) => void;
  setEvents: (events: TimelineEvent[]) => void;
  setModels: (models: ModelEntry[]) => void;
  setSnapshot: (snapshot: KGSnapshot | null) => void;
  setIsPlaying: (playing: boolean) => void;
  toggleFOL: () => void;
  setSelectedEventId: (id: string | null) => void;
}

export const useTimelineStore = create<TimelineState>((set) => ({
  currentDate: new Date(1924, 0, 1),
  brand: "all",
  productType: "all",
  industry: "soju",
  events: [],
  models: [],
  snapshot: null,
  isPlaying: false,
  folVisible: false,
  selectedEventId: null,

  setCurrentDate: (date) => set({ currentDate: date }),
  setBrand: (brand) => set({ brand }),
  setProductType: (type) => set({ productType: type }),
  setIndustry: (industry) => set({ industry }),
  setEvents: (events) => set({ events }),
  setModels: (models) => set({ models }),
  setSnapshot: (snapshot) => set({ snapshot }),
  setIsPlaying: (playing) => set({ isPlaying: playing }),
  toggleFOL: () => set((s) => ({ folVisible: !s.folVisible })),
  setSelectedEventId: (id) => set({ selectedEventId: id }),
}));
