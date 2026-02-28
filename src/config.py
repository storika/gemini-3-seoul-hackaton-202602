"""Configuration management for Soju Brand Agent."""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Google API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Gemini models
GEMINI_MODEL = "gemini-3-flash-preview"

# Media generation models
VEO_MODEL = "veo-3.1-generate-preview"
IMAGEN_MODEL = "imagen-4.0-generate-001"

# ChromaDB
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(PROJECT_ROOT / "chroma_data"))

# Temporal decay
TEMPORAL_DECAY_ALPHA = float(os.getenv("TEMPORAL_DECAY_ALPHA", "0.02"))

# Memory search
SIMILARITY_WEIGHT = 0.6
TEMPORAL_WEIGHT = 0.4
DEFAULT_SEARCH_K = 10
DEFAULT_TRIPLET_K = 20

# Brand namespaces
VALID_BRAND_NAMESPACES = {"chamisul", "chumchurum", "saero"}

# Seed data
SEED_DATA_PATH = PROJECT_ROOT / "seed_data_soju.json"
