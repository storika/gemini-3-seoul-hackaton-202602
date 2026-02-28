"use client";

import { useMemo } from "react";
import type { KGSnapshot } from "@/lib/types";
import type { ChartData, ChartOptions } from "chart.js";

const BRAND_COLORS: Record<string, { line: string; fill: string }> = {
  jinro: { line: "#1B5E20", fill: "rgba(27,94,32,0.1)" },
  chamisul: { line: "#2E7D32", fill: "rgba(46,125,50,0.1)" },
  chum_churum: { line: "#1565C0", fill: "rgba(21,101,192,0.1)" },
  saero: { line: "#F57C00", fill: "rgba(245,124,0,0.1)" },
  multi: { line: "#7B1FA2", fill: "rgba(123,31,162,0.1)" },
};

const ALPHA = 0.0003;

export function useDecayChart(
  snapshot: KGSnapshot | null,
  currentDate: Date
): { data: ChartData<"line">; options: ChartOptions<"line"> } {
  const data = useMemo<ChartData<"line">>(() => {
    if (!snapshot) return { labels: [], datasets: [] };

    const keyNodes = snapshot.nodes
      .filter((n) => n.type === "brand" || n.type === "product" || n.type === "person")
      .slice(0, 10);

    if (keyNodes.length === 0) return { labels: [], datasets: [] };

    const minDate = new Date(1924, 0, 1);
    const maxDate = currentDate;
    const labels: string[] = [];
    const timePoints: Date[] = [];
    const d = new Date(minDate);
    while (d <= maxDate) {
      labels.push(`${d.getFullYear()}`);
      timePoints.push(new Date(d));
      d.setFullYear(d.getFullYear() + 2);
    }

    const datasets = keyNodes.map((node) => {
      const addedDate = new Date(node.added_date);
      const brand = node.brand || "";
      const colors = BRAND_COLORS[brand] || { line: "#888", fill: "rgba(136,136,136,0.1)" };

      const values = timePoints.map((t) => {
        if (t < addedDate) return null;
        const daysDiff = (t.getTime() - addedDate.getTime()) / 86400000;
        return Math.exp(-ALPHA * daysDiff);
      });

      return {
        label: node.label,
        data: values,
        borderColor: colors.line,
        backgroundColor: colors.fill,
        borderWidth: node.type === "brand" ? 2 : 1,
        borderDash: node.type === "person" ? [6, 3] : node.type === "product" ? [4, 2] : [],
        pointRadius: 0,
        fill: false,
        tension: 0.3,
      };
    });

    return { labels, datasets };
  }, [snapshot, currentDate]);

  const options = useMemo<ChartOptions<"line">>(
    () => ({
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 400 },
      plugins: {
        legend: {
          display: true,
          position: "right",
          labels: {
            color: "#8b8fa3",
            font: { size: 10, family: "Inter" },
            boxWidth: 12,
            padding: 8,
          },
        },
        tooltip: {
          mode: "index",
          intersect: false,
          backgroundColor: "#1a1d27",
          borderColor: "#2a2d3a",
          borderWidth: 1,
          titleColor: "#e8e8ec",
          bodyColor: "#8b8fa3",
          titleFont: { size: 11 },
          bodyFont: { size: 10 },
        },
      },
      scales: {
        x: {
          grid: { color: "rgba(42,45,58,0.5)" },
          ticks: { color: "#8b8fa3", font: { size: 9 }, maxTicksLimit: 12 },
        },
        y: {
          min: 0,
          max: 1,
          grid: { color: "rgba(42,45,58,0.5)" },
          ticks: {
            color: "#8b8fa3",
            font: { size: 9 },
            callback: (v: any) => Number(v).toFixed(1),
          },
          title: {
            display: true,
            text: "Temporal Weight",
            color: "#8b8fa3",
            font: { size: 10 },
          },
        },
      },
      interaction: { mode: "nearest", axis: "x", intersect: false },
    }),
    []
  );

  return { data, options };
}
