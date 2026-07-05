import os
from dotenv import load_dotenv

load_dotenv()

# Qdrant
QDRANT_URL = os.getenv("QDRANT_URL", "https://42a984b3-b433-46a6-b901-65ebea1365bd.eu-central-1-0.aws.cloud.qdrant.io")
QDRANT_APY_KEY = str(os.getenv("QDRANT_API_KEY","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6YzI1NjgwMWEtOTlhMC00ZTE5LTljMjgtMGQ5ZTM5OTM5NWUwIn0.kOeZlyXGLSIPkVq0KuG5oOJGFbSXpuQIfchtNwuiIDE"))
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "experiment_02")

# Sentence transformer model
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)

# Scoring weights for hybrid recommend
ALPHA = float(os.getenv("SCORE_ALPHA", 0.67))   # cosine similarity weight
BETA  = float(os.getenv("SCORE_BETA",  0.217))   # jaccard skill weight
GAMMA = float(os.getenv("SCORE_GAMMA", 0.2))   # overlap skill weight

# How many candidates to pull from Qdrant before re-ranking
QDRANT_CANDIDATE_LIMIT = int(os.getenv("QDRANT_CANDIDATE_LIMIT", 30))

# Final top N returned to the API
TOP_N_RESULTS = int(os.getenv("TOP_N_RESULTS", 10))

# Skill extractor threshold
SKILL_SCORE_THRESHOLD = float(os.getenv("SKILL_SCORE_THRESHOLD", 0.5))