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

## Key Features

### 1. Interactive Century-Scale Timeline
Drag through 100+ years of brand history. Watch the knowledge graph grow, mutate, and evolve in real-time as events unfold — from Jinro's founding under Japanese colonial rule (1924) to AI-directed brand strategy (2026).

### 2. Dynamic Knowledge Graph Visualization
Powered by Cytoscape.js, the graph renders brand entities, people, products, campaigns, and their relationships. Temporal decay weights control node opacity — recent connections are vivid, older ones fade but persist.

### 3. Reasoning Graph (FOL Evidence Layer)
Toggle the Reasoning Graph to see causal chains explaining **why** brands succeeded at specific moments in history:
- **Soju (Korean)**: Era-contextual narratives connecting social conditions to brand decisions (e.g., "웰빙 열풍 + 참이슬 독점 피로 → 처음처럼이 파고든 시장 틈새")
- **Whisky (English)**: British and world history-grounded reasoning (e.g., "Post-Napoleonic Britain's Industrial Revolution → John Walker's blending innovation → 200-year whisky dynasty")

### 4. Multi-Industry Tabs
Switch between **SOJU**, **BEER**, and **WHISKY** industries. Each industry has its own timeline events, knowledge graph, reasoning chains, brand colors, and model gallery.

### 5. AI Campaign Generator
Generate brand campaign images (Imagen 4.0) and video ads (Veo 3.1) that are historically informed — the AI understands what worked in each era and why.

### 6. Model Gallery with Historical Profiles
Browse brand ambassadors across decades with real profile images, era context, and their impact on brand trajectory.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js 15)                  │
│  Timeline ← → KG Visualization ← → Reasoning Panel      │
│  Zustand Store │ SWR Cache │ Cytoscape.js Renderer       │
└───────────────────────┬─────────────────────────────────┘
                        │ REST API
┌───────────────────────┴─────────────────────────────────┐
│                  Backend (FastAPI + Python)               │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ Timeline API  │  │ KG Snapshot  │  │ Media Gen API │  │
│  │ (events,     │  │ (temporal    │  │ (Imagen 4.0,  │  │
│  │  models)     │  │  decay, FOL) │  │  Veo 3.1)     │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │          Temporal Knowledge Engine                │   │
│  │  Event Data → KG Mutations → FOL Evidence        │   │
│  │  Industry Filter │ Brand Filter │ Date Window     │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
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
├── agents/          # Google ADK multi-agent system
├── api/
│   └── routes/      # FastAPI endpoints (timeline, KG, media)
├── media/           # Imagen 4.0 & Veo 3.1 clients
├── memory/          # Hybrid Graph + Vector memory
└── timeline/
    ├── events.py           # Event & KGMutation data models
    ├── event_data.py       # Soju timeline (1924-2026, 16 events)
    ├── event_data_whisky.py # Whisky timeline (1820-2026, 16 events)
    ├── fol_evidence.py     # FOL reasoning chains (soju + whisky)
    ├── kg_snapshot.py      # Temporal KG builder with decay
    └── model_gallery.py    # Brand ambassador profiles

frontend/
├── src/
│   ├── app/                # Next.js App Router
│   ├── components/
│   │   ├── Header.tsx           # Industry & brand tabs
│   │   ├── KnowledgeGraph/
│   │   │   ├── KnowledgeGraph.tsx   # Main KG visualization
│   │   │   ├── ReasoningPanel.tsx   # FOL reasoning display
│   │   │   ├── useKGRenderer.ts     # Cytoscape.js renderer
│   │   │   └── NodePopup.tsx        # Node detail popup
│   │   └── Timeline/               # Timeline slider & events
│   ├── hooks/
│   │   ├── useTimelineData.ts   # SWR data fetching
│   │   └── useKGSnapshot.ts     # Debounced KG updates
│   ├── stores/
│   │   └── timeline-store.ts    # Zustand global state
│   └── lib/
│       ├── api.ts       # API client functions
│       ├── types.ts     # TypeScript interfaces
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
