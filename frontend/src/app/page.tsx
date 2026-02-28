"use client";

import Header from "@/components/Header";
import KnowledgeGraph from "@/components/KnowledgeGraph/KnowledgeGraph";
import DetailPanel from "@/components/DetailPanel/DetailPanel";
import DecayChart from "@/components/DecayChart/DecayChart";
import ModelStrip from "@/components/ModelStrip/ModelStrip";
import TimelineScrubber from "@/components/Timeline/TimelineScrubber";
import { useTimelineData } from "@/hooks/useTimelineData";
import { useKGSnapshot } from "@/hooks/useKGSnapshot";

export default function Home() {
  // Load initial data
  useTimelineData();
  // Auto-fetch KG snapshots on date/brand/fol changes
  useKGSnapshot();

  return (
    <>
      <Header />
      <main className="app-main">
        <KnowledgeGraph />
        <DetailPanel />
      </main>
      <DecayChart />
      <ModelStrip />
      <TimelineScrubber />
    </>
  );
}
