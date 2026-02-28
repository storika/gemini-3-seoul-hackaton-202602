# Green Bottle: Temporal Knowledge Reasoning for Brand Intelligence

**Live Demo: [https://greenbottle.live](https://greenbottle.live/)**

**Gemini 3.0 Seoul Hackathon 2026**

---

## The Problem: AI Branding Is Shallow

Today's AI-driven brand campaigns are optimized for **momentary traffic** — click-through rates, viral hooks, and fleeting engagement. They chase the surface and miss the soul. The result? Brands that feel disposable. Campaigns that are forgotten tomorrow.

**AI brands fail to deeply move humans** because they lack temporal depth. They have no memory of why a brand succeeded 50 years ago, no understanding of how cultural shifts shaped consumer loyalty across generations, and no reasoning about the causal chains that built iconic brands over a century.

## Our Solution: Temporal Knowledge Reasoning Graph

We apply **Temporal Knowledge Reasoning Graph** technology to give AI the depth of a century of brand knowledge.

Instead of asking "what's trending now?", we ask: **"Why did this brand succeed in this era, given the cultural context, consumer sentiment, and competitive landscape of that time?"**

The system constructs a dynamic knowledge graph that evolves across a 100–200 year timeline, powered by:

- **Temporal Decay**: Nodes and edges carry time-weighted relevance — recent events matter more, but foundational heritage never fades
- **First-Order Logic (FOL) Reasoning Chains**: Formal causal reasoning that connects era context → public sentiment → brand/model preference (e.g., "Post-IMF crisis consumers craved purity → Lee Young-ae's innocent image matched → Chamisul's 'clean soju' positioning succeeded")
- **Knowledge Graph Mutations**: Each historical event adds, modifies, or removes nodes/edges in the graph — the knowledge evolves as history unfolds
- **Multi-Industry Coverage**: Korean Soju (1924–2026, 100 years) and Scotch Whisky (1820–2026, 200 years) with full reasoning chains

---

## End-to-End Pipeline

The system is **not just a history viewer** — it's a full pipeline from century-scale brand analysis to actionable influencer campaigns.

```
 STEP 1              STEP 2               STEP 3                STEP 4               STEP 5
 HISTORY             LIVE                 DISCOVER              CREATE               OUTREACH
 ─────────────►      ─────────────►       ─────────────►        ─────────────►       ─────────────►

 Scrub 100-200yr     Temporal decay       Search micro-         Generate sample      Hyper-personalized
 timeline. KG        scores all past      influencer networks   content for the      outreach at scale.
 mutates. FOL        ambassadors →        for creators who      optimal creator      Voice calls,
 reasoning chains    "Ideal Ambassador    match the ideal       combinations.        brand guides,
 explain WHY each    DNA" composite       DNA attributes.       Imagen 4 images +    ready-to-publish
 era succeeded.      (e.g. IU 30%,        Brand Guard agent     Veo 3.1 video ads    social posts per
                     이효리 20%...)       validates brand fit.  per creator.         creator.
```

### Step 1: HISTORY — Century-Scale Temporal Reasoning

Drag through **100+ years** of brand history. The knowledge graph grows, mutates, and evolves as events unfold. FOL reasoning chains explain the causal logic behind every brand's success or failure in each era.

- **Soju** (1924–2026, Korean): 진로 설립 under Japanese colonial rule → IMF 위기가 만든 국민 소주 참이슬 → 아이유 10년 브랜드 충성도 → 새로 제로슈거 파괴적 혁신
- **Whisky** (1820–2026, English): John Walker's grocery shop → Striding Man icon → Keep Walking $2.2B campaign → Sabrina Carpenter Gen Z bridge

### Step 2: LIVE — Ideal Ambassador DNA Composite

Press the **LIVE** button to jump to 2026-02-28. The system scores **every ambassador across the entire timeline** using temporal decay and produces a weighted composite:

```
raw_score = temporal_weight × event_impact × (1 + duration_bonus)

where:
  temporal_weight = exp(-alpha × days_since_midpoint)
  event_impact    = average impact_score of matching events
  duration_bonus  = min(1.0, (end_year - start_year) / 10)
```

Same-name ambassadors are aggregated, then normalized to percentages. The result is the **"Ideal Ambassador DNA"** — a ranked breakdown showing exactly which historical attributes matter most right now.

FOL conclusions from the top-ranked ambassadors are synthesized into a composite reasoning narrative.

### Step 3: DISCOVER — Micro-Influencer Network Search

The ideal DNA attributes feed into **Storika Social Ontology** to discover real micro-influencers whose profiles match:

- **Brand Guard Agent** (Gemini 3 Flash) validates each candidate:
  - Image Lineage (40%) — does the creator's visual identity fit the brand's ambassador history?
  - CF History & Risk (30%) — past 3 years competitor overlap check
  - Visual Consistency (30%) — public aesthetic matches brand identity
- Candidates must score **> 0.70** to pass validation
- Result: a curated shortlist of creators with engagement metrics, follower data, and brand-fit reasoning

### Step 4: CREATE — AI-Generated Sample Content

For each selected creator, a **two-step AI pipeline** generates personalized content:

1. **Gemini 3 Flash** analyzes the creator's real Instagram photos — appearance, fashion style, photography mood, aesthetic fingerprint
2. **Imagen 4** generates brand-aligned content variations based on that analysis:
   - Hero shots (product + creator aesthetic)
   - Lifestyle images (natural context)
   - Intimate close-ups (product detail)
3. **Veo 3.1** generates short-form vertical video (9:16) per creator
4. **Carousel packages** with Korean text overlays for Instagram
5. **Product swap** variations — same creator aesthetic, different products for multi-brand campaigns

### Step 5: OUTREACH — Hyper-Personalized at Scale

Automated outreach pipeline per creator:

- **Voice calls** (ElevenLabs) — personalized Korean scripts per creator
- **Brand guidelines** — per-creator alignment documents
- **Ready-to-publish posts** — platform-optimized social content packages
- **Creator content kits** — all generated images, carousels, videos bundled for delivery

---

## Key Features

### Interactive Century-Scale Timeline
Drag through 100+ years of brand history. Watch the knowledge graph grow, mutate, and evolve in real-time as events unfold — from Jinro's founding under Japanese colonial rule (1924) to AI-directed brand strategy (2026).

### Dynamic Knowledge Graph Visualization
Powered by Cytoscape.js, the graph renders brand entities, people, products, campaigns, and their relationships. Temporal decay weights control node opacity — recent connections are vivid, older ones fade but persist.

### Reasoning Graph (FOL Evidence Layer)
Toggle the Reasoning Graph to see causal chains explaining **why** brands succeeded at specific moments in history:
- **Soju (Korean)**: Era-contextual narratives connecting social conditions to brand decisions (e.g., "웰빙 열풍 + 참이슬 독점 피로 → 처음처럼이 파고든 시장 틈새")
- **Whisky (English)**: British and world history-grounded reasoning (e.g., "Post-Napoleonic Britain's Industrial Revolution → John Walker's blending innovation → 200-year whisky dynasty")

### LIVE Mode: Ideal Ambassador DNA
Press LIVE to aggregate all historical ambassador data with temporal decay scoring into a composite recommendation — showing exactly which past ambassador attributes are most relevant for today's campaign.

### Multi-Industry Tabs
Switch between **SOJU**, **BEER**, and **WHISKY** industries. Each industry has its own timeline events, knowledge graph, reasoning chains, brand colors, and model gallery.

### Multi-Agent Orchestration (Google ADK)
A **Liquor Director** root agent coordinates specialized sub-agents:
- **Trend Analyzer** — searches and analyzes real-time market trends against brand memory
- **Creative Director** — generates briefs, images (Imagen 4), and videos (Veo 3.1) with brand-specific guidelines
- **Brand Guard** — validates celebrity/creator brand fit with a 0.70 threshold scoring system

### Hyper-Personalized Influencer Outreach
End-to-end pipeline from creator discovery to content delivery: voice outreach, brand guides, AI-generated per-creator content (hero, lifestyle, carousel, video), and product swap variations.

### Model Gallery with Historical Profiles
Browse brand ambassadors across decades with real profile images, era context, and their impact on brand trajectory.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Frontend (Next.js 15)                       │
│  Timeline ← → KG Visualization ← → Reasoning Panel ← → LIVE   │
│  Zustand Store │ SWR Cache │ Cytoscape.js Renderer              │
└───────────────────────────┬─────────────────────────────────────┘
                            │ REST API
┌───────────────────────────┴─────────────────────────────────────┐
│                    Backend (FastAPI + Python)                     │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  ┌────────┐  │
│  │ Timeline API │  │ KG Snapshot │  │ LIVE Rec.  │  │ Media  │  │
│  │ (events,    │  │ (temporal   │  │ (temporal  │  │ Gen API│  │
│  │  models)    │  │  decay,FOL) │  │  scoring)  │  │Imagen4 │  │
│  └─────────────┘  └─────────────┘  └────────────┘  │Veo 3.1 │  │
│                                                      └────────┘  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Temporal Knowledge Engine                    │   │
│  │  Event Data → KG Mutations → FOL Evidence → LIVE Decay   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           Google ADK Multi-Agent System                   │   │
│  │  Liquor Director → Trend Analyzer → Creative Director    │   │
│  │                  → Brand Guard (fit validation)           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │        Influencer Outreach Pipeline                       │   │
│  │  Discovery → Voice → Guidelines → Content → Carousel     │   │
│  │  Storika Social Ontology │ ElevenLabs │ Imagen 4 │ Veo   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │        Hybrid Memory (Graph + Vector)                     │   │
│  │  ChromaDB │ NetworkX │ Temporal Decay │ Consolidation     │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Google AI Stack
| Component | Technology | Role |
|-----------|-----------|------|
| Core LLM | **Gemini 3.0 Flash Preview** | Agent reasoning, data structuring, orchestration |
| Image Gen | **Imagen 4.0** | Campaign visuals, product images |
| Video Gen | **Veo 3.1** | Brand storytelling video ads |
| Agents | **Google ADK** | Multi-agent orchestration (Director, Trend Analyzer, Creative Director, Brand Guard) |

### Frontend Stack
| Component | Technology |
|-----------|-----------|
| Framework | Next.js 15 (App Router) |
| State | Zustand |
| Data Fetching | SWR |
| KG Rendering | Cytoscape.js |
| Charts | Chart.js + react-chartjs-2 |
| Deployment | Vercel |

### Backend Stack
| Component | Technology |
|-----------|-----------|
| API | FastAPI (Python) |
| KG Engine | NetworkX + custom temporal decay |
| FOL Layer | Custom first-order logic evidence chains |
| Vector Store | ChromaDB |

---

## Project Structure

```
src/
├── agents/                     # Google ADK multi-agent system
│   ├── agent.py                #   Liquor Director (root orchestrator)
│   ├── trend_analyzer/         #   Market trend search & analysis
│   ├── creative_director/      #   Imagen 4 + Veo 3.1 content generation
│   └── brand_guard/            #   Celebrity/creator brand-fit validation
├── api/
│   └── routes/                 # FastAPI endpoints (timeline, KG, media, LIVE)
├── media/                      # Imagen 4.0 & Veo 3.1 clients
├── memory/                     # Hybrid Graph + Vector memory
│   ├── memory_system.py        #   BrandMemorySystem (search, enrich, consolidate)
│   ├── graph_store.py          #   NetworkX KG per brand namespace
│   ├── vector_store.py         #   ChromaDB vector store wrapper
│   └── temporal_decay.py       #   Exponential weighted decay
└── timeline/
    ├── events.py               # Event & KGMutation data models
    ├── event_data.py           # Soju timeline (1924-2026, 16 events)
    ├── event_data_whisky.py    # Whisky timeline (1820-2026, 16 events)
    ├── fol_evidence.py         # FOL reasoning chains (32 events, soju + whisky)
    ├── kg_snapshot.py          # Temporal KG builder + LIVE recommendation engine
    └── model_gallery.py        # 70+ ambassador profiles across 25+ products

scripts/
└── outreach/                   # Hyper-personalized influencer outreach pipeline
    ├── creators.py             #   Creator discovery (Storika Social Ontology)
    ├── generate_creator_content.py  # Gemini analysis + Imagen 4 content gen
    ├── generate_voice.py       #   ElevenLabs personalized Korean voice calls
    ├── generate_guidelines.py  #   Per-creator brand alignment guides
    ├── generate_posts.py       #   Ready-to-publish social content
    ├── generate_carousel.py    #   Imagen 4 multi-slide carousels
    ├── generate_video.py       #   Veo 3.1 short-form vertical video
    ├── product_swap.py         #   Same aesthetic, different products
    └── demo.py                 #   Interactive 8-step pipeline walkthrough

frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   ├── components/
│   │   ├── Header.tsx               # Industry & brand tabs
│   │   ├── KnowledgeGraph/
│   │   │   ├── KnowledgeGraph.tsx   # KG visualization + LIVE mode
│   │   │   ├── ReasoningPanel.tsx   # FOL reasoning + LIVE ambassador bars
│   │   │   ├── useKGRenderer.ts     # Cytoscape.js renderer
│   │   │   └── NodePopup.tsx        # Node detail popup
│   │   └── Timeline/               # Timeline slider + LIVE button
│   ├── hooks/
│   │   ├── useTimelineData.ts   # SWR data fetching
│   │   └── useKGSnapshot.ts     # Debounced KG updates
│   ├── stores/
│   │   └── timeline-store.ts   # Zustand state (+ liveMode, liveRecommendation)
│   └── lib/
│       ├── api.ts       # API client (+ fetchLiveRecommendation)
│       ├── types.ts     # TypeScript interfaces (+ Live* types)
│       └── constants.ts # Brand colors & config
```

---

## Getting Started

### 1. Environment Setup
```bash
cp .env.example .env
# Set GOOGLE_API_KEY (Gemini 3.0, Imagen, Veo permissions required)
```

### 2. Backend
```bash
pip install -r requirements.txt
pip install -e .
uvicorn src.api.server:app --host 0.0.0.0 --port 8001 --reload
```

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

### 4. Vercel Deployment
Set the **Root Directory** to `frontend` in Vercel project settings. Add environment variable:
```
API_URL=http://<your-backend-ip>:8001
```

---

## Temporal Knowledge Reasoning: How It Works

### 1. Knowledge Graph Mutations
Each timeline event carries `kg_mutations` — instructions to add/remove nodes and edges:
```python
# When "Chamisul Revolution (1998)" event fires:
add_node("chamisul", "brand", "Chamisul (참이슬)")
add_node("bamboo_charcoal", "technology", "Bamboo Charcoal Purification")
add_edge("chamisul", "bamboo_charcoal", "USES_TECHNOLOGY")
```

### 2. Temporal Decay
All nodes/edges carry a `temporal_weight` that decays over time:
```
weight = exp(-alpha * |current_date - event_date|)
```
Recent events dominate the graph; older ones fade but persist — just like cultural memory.

### 3. FOL Reasoning Chains
Each event has formal reasoning: `Predicates → Rule → Conclusion`

**Soju Example** (Korean narrative):
> *"IMF 외환위기, 대중은 불안과 좌절 속에서 저렴한 위안을 갈구했다"*
> → *"깨끗함이라는 메시지가 위기에 지친 소비자의 마음을 정화시켰다"*
> → *"참이슬 6개월 만에 1억병 돌파. 위기가 만든 국민 소주의 탄생"*

**Whisky Example** (English narrative):
> *"1999 — the world stood between millennium anxiety and dot-com euphoria. 'Keep Walking' captured the zeitgeist"*
> → *"Millennial zeitgeist × authentic celebrity × visual reinvention → not an ad campaign, but a cultural movement"*
> → *"$2.2 billion in incremental sales over a decade"*

---

## Research References

This project draws on cutting-edge research in temporal knowledge graph reasoning, long-term knowledge representation, and neural-symbolic AI:

1. **A Survey on Temporal Knowledge Graph: Representation Learning and Applications** (2024)
   Cai et al. — Comprehensive survey covering TKGE methods across seven categories.
   [https://arxiv.org/abs/2403.04782](https://arxiv.org/abs/2403.04782)

2. **TKG-Thinker: Towards Dynamic Reasoning over Temporal Knowledge Graphs via Agentic Reinforcement Learning** (2025)
   Multi-turn temporal reasoning with autonomous planning and adaptive retrieval via dual-training strategy (SFT + RL).
   [https://arxiv.org/abs/2602.05818](https://arxiv.org/abs/2602.05818)

3. **Selective Temporal Knowledge Graph Reasoning** (2024)
   Liu et al. — Selective reasoning over temporally evolving facts for future event prediction.
   [https://arxiv.org/abs/2404.01695](https://arxiv.org/abs/2404.01695)

4. **A Unified Temporal Knowledge Graph Reasoning Model Towards Interpolation and Extrapolation (TPAR)** (2024)
   Neural-symbolic temporal path-based reasoning applicable to both interpolation and extrapolation.
   [https://arxiv.org/abs/2405.18106](https://arxiv.org/abs/2405.18106)

5. **Temporal Reasoning over Evolving Knowledge Graphs (EvoReasoner)** (2025)
   Temporal-aware multi-hop reasoning with global-local entity grounding and temporally grounded scoring.
   [https://arxiv.org/abs/2509.15464](https://arxiv.org/abs/2509.15464)

6. **Temporal Retrieval-Augmented Generation via Graph** (2025)
   Under review at ICLR 2026 — Combines temporal knowledge graphs with retrieval-augmented generation.
   [https://arxiv.org/abs/2510.16715](https://arxiv.org/abs/2510.16715)

7. **Temporal Knowledge Graph Reasoning With Dynamic Memory Enhancement** (2024)
   Zhang et al. — Dynamic memory mechanisms for temporal KG reasoning.
   [https://doi.org/10.1109/TNNLS.2024.3382864](https://doi.org/10.1109/TNNLS.2024.3382864)

8. **A Survey on Temporal Knowledge Graph Embedding: Models and Applications** (2024)
   Published in Knowledge-Based Systems — Systematic review of TKGE models and downstream applications.
   [https://doi.org/10.1016/j.knosys.2024.112454](https://doi.org/10.1016/j.knosys.2024.112454)

---

## License

MIT
