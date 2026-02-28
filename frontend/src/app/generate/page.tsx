"use client";

import { useState, useMemo, useCallback, useEffect, useRef } from "react";
import Link from "next/link";
import { useTimelineStore } from "@/stores/timeline-store";
import seedData from "../../../../data/seed_model_vectors.json";
import creatorsKR from "../../../../data/vectorized_instagram_kr_creators_sample100.json";
import creatorsGB from "../../../../data/vectorized_instagram_creators_sample100.json";

/* ── types ── */
interface CreatorData {
  creator_id: string;
  metadata: { primary_platform: string; follower_count: number; main_category: string };
  visual_persona_deep: {
    beauty_archetype: Record<string, number>;
    facial_feature_details: {
      eye_vibe: string;
      smile_type: string;
      face_shape_index: string;
      skin_texture_spec: Record<string, number>;
    };
    color_harmony_vector: {
      seasonal_type: string;
      dominant_tone: string;
      contrast_preference: number;
    };
  };
  brand_fit_logic: {
    soju_affinity_matrix: Record<string, number>;
    kbeauty_role_suitability: string[];
  };
  temporal_evolution_compatibility: Record<string, number>;
  risk_management: { brand_safety_score: number; competitor_overlap_index: number };
}

/* ── vector keys ── */
const ARCHETYPE_KEYS = [
  "pure_innocent", "moody_cinematic", "chic_cold", "sultry_alluring",
  "lovely_juicy", "quirky_individualistic", "elegant_classic", "royal_noble",
  "hip_crush", "androgynous_neutral", "healthy_vitality", "intellectual_calm",
  "vintage_analog", "cyber_virtual_perfect",
];
const SKIN_KEYS = ["glass_skin_level", "velvet_matte_level", "natural_texture_index"];
const SOJU_KEYS = [
  "chamisul_clean_index", "chumchurum_soft_index", "saero_zero_hip_index",
  "jinro_retro_index", "premium_single_malt_index",
];
const ERA_KEYS = [
  "era_1924_1950_classic", "era_1960_1980_industrial",
  "era_1990_2010_digital_y2k", "era_2020_2026_future_meta",
];

function toVector(c: CreatorData): number[] {
  const arch = ARCHETYPE_KEYS.map((k) => c.visual_persona_deep.beauty_archetype[k] ?? 0);
  const skin = SKIN_KEYS.map((k) => c.visual_persona_deep.facial_feature_details.skin_texture_spec[k] ?? 0);
  const contrast = [c.visual_persona_deep.color_harmony_vector.contrast_preference ?? 0];
  const soju = SOJU_KEYS.map((k) => c.brand_fit_logic.soju_affinity_matrix[k] ?? 0);
  const era = ERA_KEYS.map((k) => c.temporal_evolution_compatibility[k] ?? 0);
  const risk = [c.risk_management.brand_safety_score, c.risk_management.competitor_overlap_index];
  return [...arch, ...skin, ...contrast, ...soju, ...era, ...risk];
}

function cosineSim(a: number[], b: number[]): number {
  let dot = 0, magA = 0, magB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    magA += a[i] * a[i];
    magB += b[i] * b[i];
  }
  const denom = Math.sqrt(magA) * Math.sqrt(magB);
  return denom === 0 ? 0 : dot / denom;
}

/* ── celebrity display names & reverse lookup ── */
const CELEB_DISPLAY: Record<string, string> = {
  "IU_아이유": "IU 아이유",
  "GongYoo_공유": "공유",
  "Karina_카리나": "카리나",
  "SonSukKu_손석구": "손석구",
  "Jennie_제니": "제니",
  "BaekJongWon_백종원": "백종원",
  "AnSungJae_안성재": "안성재",
  "Suzy_수지": "수지",
  "JoInSung_조인성": "조인성",
  "LeeHyori_이효리": "이효리",
};

const NAME_TO_ID: Record<string, string> = {};
for (const [id, display] of Object.entries(CELEB_DISPLAY)) {
  const parts = display.split(" ");
  parts.forEach((p) => { NAME_TO_ID[p] = id; });
  NAME_TO_ID[display] = id;
  NAME_TO_ID[id] = id;
}

const CELEB_COLORS = [
  "#E040FB", "#7C4DFF", "#00BCD4", "#FF5722", "#FFEB3B",
  "#8BC34A", "#FF4081", "#448AFF", "#FF6E40", "#69F0AE",
];

const REGION_DATA: Record<string, CreatorData[]> = {
  KR: creatorsKR as unknown as CreatorData[],
  GB: creatorsGB as unknown as CreatorData[],
};

// Video mapping: creator handle → video path
const CREATOR_VIDEOS: Record<string, string> = {
  "@jungha.0": "/creator-videos/jungha.0/jungha.0_boksoondoga.mp4",
  "@jayeonkim_": "/creator-videos/jayeonkim_/jayeonkim__boksoondoga.mp4",
  "@hwajung95": "/creator-videos/hwajung95/hwajung95_boksoondoga.mp4",
  "@bling_cuh__": "/creator-videos/bling_cuh__/bling_cuh___boksoondoga.mp4",
};

function fmtFollowers(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`;
  return String(n);
}

function topArchetypes(arch: Record<string, number>, n = 3): string[] {
  return Object.entries(arch)
    .sort((a, b) => b[1] - a[1])
    .slice(0, n)
    .map(([k]) => k.replace(/_/g, " "));
}

function igUrl(creatorId: string): string {
  const handle = creatorId.startsWith("@") ? creatorId.slice(1) : creatorId;
  return `https://www.instagram.com/${handle}/`;
}

/* ── main component ── */
export default function GeneratePage() {
  const celebrities = seedData as unknown as CreatorData[];

  const liveRecommendation = useTimelineStore((s) => s.liveRecommendation);
  const hasLiveData = !!liveRecommendation && liveRecommendation.ambassadors.length > 0;

  const [region, setRegion] = useState<"KR" | "GB">("KR");
  const [videoModal, setVideoModal] = useState<string | null>(null);
  const creators = REGION_DATA[region];

  // weights: 0..100 per celebrity
  const [weights, setWeights] = useState<Record<string, number>>(() => {
    const init: Record<string, number> = {};
    celebrities.forEach((c) => { init[c.creator_id] = 0; });
    return init;
  });

  // Auto-apply LIVE ambassador data on mount
  const appliedRef = useRef(false);
  useEffect(() => {
    if (hasLiveData && !appliedRef.current) {
      appliedRef.current = true;
      const newWeights: Record<string, number> = {};
      celebrities.forEach((c) => { newWeights[c.creator_id] = 0; });
      for (const amb of liveRecommendation.ambassadors) {
        const matchedId = NAME_TO_ID[amb.name];
        if (matchedId && matchedId in newWeights) {
          newWeights[matchedId] = Math.round(amb.percent);
        }
      }
      setWeights(newWeights);
    }
  }, [hasLiveData, liveRecommendation, celebrities]);

  const setWeight = useCallback((id: string, val: number) => {
    setWeights((prev) => ({ ...prev, [id]: val }));
  }, []);

  const celebVectors = useMemo(() => {
    const map: Record<string, number[]> = {};
    celebrities.forEach((c) => { map[c.creator_id] = toVector(c); });
    return map;
  }, [celebrities]);

  const creatorVectors = useMemo(() => {
    return creators.map((c) => ({ id: c.creator_id, vec: toVector(c) }));
  }, [creators]);

  const hasActiveWeights = Object.values(weights).some((w) => w > 0);

  const rankedCreators = useMemo(() => {
    if (!hasActiveWeights) return [];
    const totalW = Object.values(weights).reduce((s, w) => s + w, 0);
    if (totalW === 0) return [];

    const dim = creatorVectors[0]?.vec.length ?? 0;
    const target = new Array(dim).fill(0);

    for (const celeb of celebrities) {
      const w = weights[celeb.creator_id] / totalW;
      if (w === 0) continue;
      const cv = celebVectors[celeb.creator_id];
      for (let i = 0; i < dim; i++) target[i] += cv[i] * w;
    }

    return creatorVectors
      .map(({ id, vec }) => ({ id, score: cosineSim(target, vec) }))
      .sort((a, b) => b.score - a.score)
      .slice(0, 20);
  }, [weights, hasActiveWeights, celebrities, celebVectors, creatorVectors]);

  const creatorMap = useMemo(() => {
    const map: Record<string, CreatorData> = {};
    creators.forEach((c) => { map[c.creator_id] = c; });
    return map;
  }, [creators]);

  const activeCelebs = celebrities.filter((c) => weights[c.creator_id] > 0);
  const totalWeight = Object.values(weights).reduce((s, w) => s + w, 0);

  return (
    <div className="gen-page">
      <header className="app-header">
        <h1>Creator Generate</h1>
        <nav className="type-tabs">
          <Link href="/" className="type-tab">DASHBOARD</Link>
          <span className="type-tab active">GENERATE</span>
        </nav>

        {/* Region tabs */}
        <nav className="brand-tabs">
          {(["KR", "GB"] as const).map((r) => (
            <button
              key={r}
              className={`brand-tab${region === r ? " active" : ""}`}
              onClick={() => setRegion(r)}
            >
              {r === "KR" ? "KR" : "GB"}
            </button>
          ))}
        </nav>

        <div className="gen-subtitle-wrap">
          <span className="gen-subtitle">
            {hasLiveData ? "LIVE 분석 결과 기반" : "연예인 벡터 믹싱으로 크리에이터 탐색"}
          </span>
        </div>
        <div className="date-display">
          {activeCelebs.length > 0 ? `${activeCelebs.length}명 선택` : "Mix Ready"}
        </div>
      </header>

      <div className="gen-layout">
        {/* left: celebrity sliders */}
        <aside className="gen-sidebar">
          <h2 className="gen-section-title">Celebrity Axes</h2>
          <p className="gen-hint">
            {hasLiveData
              ? "LIVE 결과가 슬라이더에 반영되었습니다. 자유롭게 조절하세요"
              : "슬라이더를 조절해서 원하는 페르소나를 믹싱하세요"}
          </p>

          {celebrities.map((celeb, idx) => {
            const w = weights[celeb.creator_id];
            const color = CELEB_COLORS[idx % CELEB_COLORS.length];
            return (
              <div key={celeb.creator_id} className={`gen-slider-row ${w > 0 ? "active" : ""}`}>
                <div className="gen-slider-header">
                  <span className="gen-celeb-dot" style={{ background: color }} />
                  <span className="gen-celeb-name">{CELEB_DISPLAY[celeb.creator_id] ?? celeb.creator_id}</span>
                  <span className="gen-celeb-cat">{celeb.metadata.main_category}</span>
                  <span className="gen-slider-val">{w}</span>
                </div>
                <input
                  type="range"
                  min={0}
                  max={100}
                  value={w}
                  onChange={(e) => setWeight(celeb.creator_id, Number(e.target.value))}
                  className="gen-slider"
                  style={{ "--slider-color": color } as React.CSSProperties}
                />
                {w > 0 && (
                  <div className="gen-celeb-tags">
                    {topArchetypes(celeb.visual_persona_deep.beauty_archetype).map((t) => (
                      <span key={t} className="gen-tag" style={{ borderColor: color }}>{t}</span>
                    ))}
                  </div>
                )}
              </div>
            );
          })}

          {hasActiveWeights && (
            <button className="gen-reset" onClick={() => {
              const reset: Record<string, number> = {};
              celebrities.forEach((c) => { reset[c.creator_id] = 0; });
              setWeights(reset);
            }}>
              Reset All
            </button>
          )}
        </aside>

        {/* right: results */}
        <main className="gen-results">
          {!hasActiveWeights ? (
            <div className="gen-empty">
              <div className="gen-empty-icon">&#x1f3af;</div>
              <h3>슬라이더를 조절해 보세요</h3>
              <p>연예인 비율을 조합하면 비슷한 크리에이터를 찾아드립니다</p>
            </div>
          ) : (
            <>
              <div className="gen-mix-bar">
                <span className="gen-mix-label">Current Mix</span>
                <div className="gen-mix-chips">
                  {activeCelebs.map((c) => {
                    const pct = totalWeight > 0 ? Math.round((weights[c.creator_id] / totalWeight) * 100) : 0;
                    const ci = celebrities.indexOf(c);
                    return (
                      <span key={c.creator_id} className="gen-mix-chip" style={{ background: CELEB_COLORS[ci] + "33", borderColor: CELEB_COLORS[ci] }}>
                        {CELEB_DISPLAY[c.creator_id]} {pct}%
                      </span>
                    );
                  })}
                </div>
              </div>

              <div className="gen-grid">
                {rankedCreators.map((rc, idx) => {
                  const c = creatorMap[rc.id];
                  if (!c) return null;
                  const tops = topArchetypes(c.visual_persona_deep.beauty_archetype);
                  return (
                    <div key={rc.id} className="gen-card">
                      <div className="gen-card-rank">#{idx + 1}</div>
                      <div className="gen-card-header">
                        <a
                          href={igUrl(c.creator_id)}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="gen-card-avatar"
                          title="Instagram 프로필 보기"
                        >
                          {c.creator_id.replace("@", "").slice(0, 2).toUpperCase()}
                        </a>
                        <div className="gen-card-info">
                          <h4>
                            <a
                              href={igUrl(c.creator_id)}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="gen-card-link"
                            >
                              {c.creator_id}
                            </a>
                          </h4>
                          <span className="gen-card-meta">
                            {c.metadata.main_category} · {fmtFollowers(c.metadata.follower_count)}
                          </span>
                        </div>
                        <div className="gen-card-score">
                          <span className="gen-score-num">{(rc.score * 100).toFixed(1)}</span>
                          <span className="gen-score-label">match</span>
                        </div>
                      </div>
                      <div className="gen-sim-track">
                        <div className="gen-sim-fill" style={{ width: `${rc.score * 100}%` }} />
                      </div>
                      <div className="gen-card-tags">
                        {tops.map((t) => (
                          <span key={t} className="gen-card-tag">{t}</span>
                        ))}
                        <span className="gen-card-tag season">{c.visual_persona_deep.color_harmony_vector.seasonal_type.replace("_", " ")}</span>
                      </div>
                      <div className="gen-card-affinity">
                        {Object.entries(c.brand_fit_logic.soju_affinity_matrix).slice(0, 3).map(([k, v]) => (
                          <div key={k} className="gen-affinity-row">
                            <span className="gen-affinity-label">{k.replace(/_index$/, "").replace(/_/g, " ")}</span>
                            <div className="gen-affinity-track">
                              <div className="gen-affinity-fill" style={{ width: `${(v as number) * 100}%` }} />
                            </div>
                          </div>
                        ))}
                      </div>
                      <div className="gen-card-footer">
                        <span className="gen-safety" data-level={c.risk_management.brand_safety_score >= 0.8 ? "high" : c.risk_management.brand_safety_score >= 0.6 ? "mid" : "low"}>
                          Safety {(c.risk_management.brand_safety_score * 100).toFixed(0)}%
                        </span>
                        <span className="gen-overlap">Overlap {(c.risk_management.competitor_overlap_index * 100).toFixed(0)}%</span>
                      </div>
                      {CREATOR_VIDEOS[c.creator_id] ? (
                        <button
                          className="gen-video-btn has-video"
                          onClick={() => setVideoModal(CREATOR_VIDEOS[c.creator_id])}
                        >
                          ▶ AI 비디오 보기
                        </button>
                      ) : (
                        <button className="gen-video-btn" disabled>
                          ▶ AI 비디오 보기
                        </button>
                      )}
                    </div>
                  );
                })}
              </div>
            </>
          )}
        </main>
      </div>
      {/* Video Modal */}
      {videoModal && (
        <div className="gen-video-overlay" onClick={() => setVideoModal(null)}>
          <div className="gen-video-modal" onClick={(e) => e.stopPropagation()}>
            <button className="gen-video-close" onClick={() => setVideoModal(null)}>&times;</button>
            <video controls autoPlay src={videoModal} className="gen-video-player" />
          </div>
        </div>
      )}
    </div>
  );
}
