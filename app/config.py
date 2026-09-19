"""
Central configuration for the AI Travel Planning Assistant.

All tunables (model names, paths, destination coordinates, API bases) live
here so the rest of the app never hard-codes them.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
RAW_DOCS_DIR = BASE_DIR / "data" / "raw"

VECTORSTORE_DIR = Path(os.getenv("VECTORSTORE_DIR", BASE_DIR / "data" / "vectorstore"))

CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

#CURRENCY_API_BASE = os.getenv("CURRENCY_API_BASE", "https://api.exchangerate.host")
#CURRENCY_API_BASE = os.getenv("CURRENCY_API_BASE", "https://api.frankfurter.dev/v2")
CURRENCY_API_BASE = os.getenv("CURRENCY_API_BASE", "https://api.frankfurter.dev/v1")
WEATHER_API_BASE = os.getenv("WEATHER_API_BASE", "https://api.open-meteo.com/v1/forecast")

DESTINATION_NAME = os.getenv("DESTINATION_NAME", "Singapore")
DESTINATION_LAT = float(os.getenv("DESTINATION_LAT", "1.3521"))
DESTINATION_LON = float(os.getenv("DESTINATION_LON", "103.8198"))

# Retrieval settings
RAG_CHUNK_SIZE = 800
RAG_CHUNK_OVERLAP = 120
RAG_TOP_K = 4
