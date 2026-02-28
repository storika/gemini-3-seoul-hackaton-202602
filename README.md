# Soju Wars: 100-Year Brand Evolution

**Gemini 3.0 Seoul Hackathon 2026**

This project is a multi-agent system that visualizes the 100-year history (1924–2026) of the Korean Soju market, analyzes brand evolution and marketing trends, and generates new brand strategies and creative content using AI agents.

---

## 🏗️ Project Architecture & Google Stack

The project is built entirely on the latest Google AI technology stack.

### 1. Multi-Agent Orchestration: Google ADK (Agent Development Kit)
We used the Google ADK to build specialized agents that autonomously perform complex workflows:
- **Root Agent (Soju Director)**: Orchestrates the entire system using `LlmAgent`, routing user requests to the appropriate sub-agents.
- **Trend Analyzer**: Combines `SequentialAgent` with the `google_search` tool to research real-time market trends and historical context.
- **Creative Director**: Integrated with `imagen-4.0` and `veo-3.1` to generate images and video ad synopses aligned with brand identity.
- **Brand Guard**: Uses `LlmAgent` to verify that generated content matches historical brand facts (e.g., specific ambassadors or alcohol percentages for a given year), preventing hallucinations.

### 2. Core LLM: Gemini 3.0 Flash Preview
**Gemini 3.0 Flash Preview** serves as the brain for all agents:
- **Features**: Its ultra-fast inference and expanded context window allow for real-time analysis of 100 years of extensive brand data.
- **Usage**: Handles complex reasoning, data structuring (Graph-to-Text), and sophisticated orchestration between agents.

### 3. Generative Media: Imagen 4.0 & Veo 3.1
We utilize the latest media generation models to recreate the past and propose the future of brands:
- **Imagen 4.0**: Generates high-resolution product images and lifestyle campaign visuals.
- **Veo 3.1**: Produces high-quality short-form video ads for brand storytelling.
- **Integration**: Directly interfaced via the `google-genai` SDK to automate prompt optimization and asset management.

### 4. Advanced RAG: Hybrid Memory System
- **Vector Store (ChromaDB)**: Extracts relevant information through semantic search.
- **Knowledge Graph (NetworkX)**: Precisely tracks relationships between entities (Brand-Model-Event).
- **Temporal Decay**: Calculates information importance over time, providing Gemini with the most relevant context based on the active timeline date.

---

## 🌟 Key Features

1. **Interactive 100-Year Timeline**: Explore the evolution of Soju brands from 1924 to 2026 in real-time.
2. **Dynamic Knowledge Graph**: Visualize how brand knowledge networks expand and connect over a century.
3. **AI Campaign Generator**: Instantly generate ad images and videos reflecting trends from specific historical periods.
4. **Hallucination-Free Guardrail**: The Brand Guard agent cross-references all generated output against historical seed data for factual accuracy.

---

## 📂 Project Structure
- `src/agents/`: Multi-agent logic based on Google ADK.
- `src/media/`: Client interfaces for Imagen and Veo.
- `src/memory/`: Hybrid memory combining Graph and Vector DBs.
- `src/api/`: Backend powered by FastAPI.
- `frontend/`: Next.js-based timeline visualization interface.
- `GEMINI.md`: Technical deep-dive and agent design specifications.

---

## 🚀 Getting Started

1. **Environment Setup**:
   ```bash
   cp .env.example .env
   # Enter your GOOGLE_API_KEY (Requires Gemini 3.0, Imagen, and Veo permissions)
   ```

2. **Installation**:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

3. **Run Server**:
   ```bash
   python -m src.api.server
   ```

4. **Run Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
