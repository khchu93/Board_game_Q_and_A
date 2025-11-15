"""
Configuration settings for the RAG evaluation system.
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

try:
    if "OPENAI_API_KEY" in st.secrets:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
except:
    # Fallback to .env file for local development
    load_dotenv()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Paths
DATA_DIR = Path("data/BoardGamesRuleBook")
PDF_PATH = DATA_DIR / "CATAN.pdf"
# TRAINING_QA_PATH = DATA_DIR / "CATAN_eval_test.json" # retrieval eval set
TRAINING_QA_PATH = DATA_DIR / "CATAN_eval_long.json"   # generation eval set

# Model settings
EMBEDDING_MODEL = "text-embedding-ada-002"
LLM_MODEL = "gpt-3.5-turbo"
LLM_TEMPERATURE = 0
SIMILARITY_SEARCH = "cosine"

# Chunking parameters (demo.py and streamlit_app.py)
DEMO_CHUNK_SIZE = 125
DEMO_CHUNK_OVERLAP = 120
DEMO_TOP_K = 5

# Evaluation parameters (run_evaluation.py)
CHUNK_SIZES = [125]
CHUNK_OVERLAPS = [120]
TOP_K_VALUES = [5]

# Prompt template
PROMPT_TEMPLATE = "default"