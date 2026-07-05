from initializer import get_model, get_qdrant_client, get_skill_extractor, get_skill_db
from query_preparer import QueryPreparer
from recommender import RecommendationEngine
from config_engine import QDRANT_COLLECTION


def recommend_for_cv(
    cv_text: str,
    cv_id: str,
    hybrid: bool = True,
) -> dict:
    """
    Public entry point called by the Celery task.

    Args:
        cv_text:         Raw plain text of the uploaded CV
        cv_id:           Unique ID for this CV (task_id works fine)
        hybrid:          True = cosine + skill re-ranking
                         False = pure vector search only

    Returns:
        {
            "job_ids": [job_id, ...],          # ordered best → worst
            "scores":  [(job_id, score), ...]  # only present in hybrid mode
        }
    """
    # 1. Initialise all dependencies (cached after first call)
    model           = get_model()
    qdrant_client   = get_qdrant_client()
    skill_extractor = get_skill_extractor()
    skill_db        = get_skill_db()
    # 2. Build the query dict for this single CV
    preparer = QueryPreparer(model, skill_extractor, skill_db)
    queries  = preparer.prepare_single(cv_id, cv_text)
    # queries = { cv_id: { "skills": {...}, "embedding": array } }

    # 3. Run recommendation
    engine = RecommendationEngine(qdrant_client, QDRANT_COLLECTION)
    if hybrid:
        results = engine.recommend_hybrid(queries)

    else:
        results = engine.recommend(queries)

    # 4. Return just this CV's results (unwrap the cv_id key)
    return results.get(cv_id, {"job_ids": [], "scores": []})