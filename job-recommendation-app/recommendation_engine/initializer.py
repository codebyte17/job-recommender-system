from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from config_engine import QDRANT_URL, QDRANT_APY_KEY, EMBEDDING_MODEL
import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor

_model = None
_qdrant_client = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print(f"[engine] Loading embedding model: {EMBEDDING_MODEL}")
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def get_qdrant_client() -> QdrantClient:
    global _qdrant_client
    if _qdrant_client is None:
        print(f"[engine] Connecting to Qdrant at {QDRANT_URL}")
        _qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_APY_KEY)
    return _qdrant_client


def get_skill_extractor():
    """
    Replace the body of this function with however you initialise
    your skill extractor (esco, skillNer, etc.)
    The interface must have an .annotate(text) method.
    """
    nlp = spacy.load("en_core_web_sm")

    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
    if skill_extractor is None:
        # ── replace with your actual skill extractor init ──
        # e.g. from skillner import SkillExtractor
        #      _skill_extractor = SkillExtractor(...)
        raise NotImplementedError(
            "Plug in your skill extractor here in initializer.py"
        )
    return skill_extractor


def get_skill_db() -> dict:
    """
    Returns the skill database dict: { skill_id: { "skill_name": str } }
    Replace with however you load your skill DB.
    """
    if SKILL_DB is None:
        # e.g. load from a JSON file or your library's built-in DB
        raise NotImplementedError(
            "Plug in your skill DB loader here in initializer.py"
        )
    return SKILL_DB