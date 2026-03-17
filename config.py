import os
from dotenv import load_dotenv

load_dotenv()

VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./vector_db")
SEMANTIC_WEIGHT = float(os.getenv("SEMANTIC_WEIGHT", 0.7))
BM25_WEIGHT = float(os.getenv("BM25_WEIGHT", 0.3))
TOP_K = 10

# The 4 categories: Weights MUST sum to 1.0
SKILL_WEIGHTS = {
    "must_have": 0.45,
    "important": 0.25,
    "nice_to_have": 0.15,
    "implicit": 0.15
}