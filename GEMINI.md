# Soju Wars: 100-Year Brand Evolution

A multi-agent system built for the Gemini 3 Seoul Hackathon (2026). This project visualizes and manages the evolution of Korean Soju brands (Chamisul, Chum Churum, Saero) through 100 years of history (1924-2026), leveraging historical data to ground creative AI agents.

## 🚀 Architecture

### 1. Multi-Agent Orchestration (ADK)
The system uses the **Google Agent Development Kit (ADK)** to manage specialized agents:
- **Liquor Director (Root Agent)**: Orchestrates the overall workflow and routes requests.
- **Trend Analyzer**: Researches market trends and historical context.
- **Creative Director**: Generates visual content (images via Imagen, videos via Veo).
- **Brand Guard**: Ensures brand consistency and prevents factual hallucinations (e.g., matching the correct celebrity ambassador to the correct year/brand).

### 2. Hybrid Memory System (A-Mem/Memoria)
Combines multiple storage strategies for robust RAG:
- **Vector Store (ChromaDB)**: For semantic similarity and fast retrieval of related facts.
- **Knowledge Graph (NetworkX)**: For relational context (e.g., "IU → Chamisul → 2014-2026").
- **Temporal Decay**: A custom weighting system that prioritizes or contextualizes data based on its historical distance from the "active" timeline date.

### 3. Timeline Visualization
A FastAPI-powered web interface that provides:
- **Interactive Timeline**: Scrub through 100 years of brand history.
- **Dynamic KG Renderer**: Visualizes the brand's knowledge network evolving over time.
- **Media Panel**: Displays historical and AI-generated ads/campaigns.
- **Decay Chart**: Visualizes how information relevance changes across time.

## 🛠 Tech Stack
- **Backend**: Python, FastAPI, Google ADK
- **AI/LLM**: Gemini 3.0 Flash Preview, Imagen 3, Veo
- **Memory**: NetworkX (Graph), ChromaDB (Vector)
- **Frontend**: Vanilla JS, CSS (Responsive SPA)

## 📂 Project Structure
- `src/agents/`: Agent definitions and tool implementations.
- `src/memory/`: Hybrid memory system (graph + vector + decay).
- `src/api/`: FastAPI routes and server logic.
- `src/web/`: Frontend timeline visualization.
- `seed_data_soju.json`: The "Source of Truth" for the 100-year history.

## 🏃 Getting Started
1. Install dependencies: `pip install -e .`
2. Set up `.env` with `GOOGLE_API_KEY`.
3. Run the server: `python -m src.api.server`
4. Open `http://localhost:8000` to view the timeline.
