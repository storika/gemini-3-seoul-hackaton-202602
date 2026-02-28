"use client";

import { useEffect, useRef } from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";
import { useTimelineStore } from "@/stores/timeline-store";
import { useDecayChart } from "./useDecayChart";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

export default function DecayChart() {
  const snapshot = useTimelineStore((s) => s.snapshot);
  const currentDate = useTimelineStore((s) => s.currentDate);
  const { data, options } = useDecayChart(snapshot, currentDate);

  return (
    <section className="decay-section">
      <Line data={data} options={options} />
    </section>
  );
}
