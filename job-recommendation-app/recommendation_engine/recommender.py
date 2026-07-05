from qdrant_client.models import Filter, FieldCondition, MatchAny
from config_engine import ALPHA, BETA, GAMMA, QDRANT_CANDIDATE_LIMIT, TOP_N_RESULTS


class RecommendationEngine:
    """
    Queries Qdrant with a CV embedding, re-ranks results
    using a hybrid cosine + Jaccard + overlap score.
    """

    def __init__(self, client, collection_name: str):
        self.client = client
        self.collection_name = collection_name

    # ── Scoring helpers ──────────────────────────────────────────────

    def jaccard(self, a: set, b: set) -> float:
        if not a or not b:
            return 0.0
        return len(a & b) / len(a | b)

    def overlap(self, a: set, b: set) -> float:
        if not a:
            return 0.0
        return len(a & b) / len(a)

    # ── Query filter builder ─────────────────────────────────────────

    def _build_filter(self, job_ids_filter: list) -> Filter:
        return Filter(
            must=[
                FieldCondition(
                    key="job_id",
                    match=MatchAny(any=job_ids_filter),
                )
            ]
        )

    def _clean_job_id(self, job_id: str) -> str:
        """Strip JOB_ prefix if present."""
        if isinstance(job_id, str) and job_id.startswith("JOB_"):
            return job_id.replace("JOB_", "")
        return job_id

    # ── Recommend methods ────────────────────────────────────────────

    def recommend_hybrid(self, queries: dict) -> dict:
        """
        Hybrid scoring: cosine similarity + Jaccard + overlap.
        Weights controlled by ALPHA, BETA, GAMMA in config.py.

        Args:
            queries:         { cv_id: { "skills": set, "embedding": np.array } }
        Returns:
            {
                cv_id: {
                    "job_ids": [job_id, ...],
                    "scores":  [(job_id, score), ...]
                }
            }
        """
        results_dict = {}
        for cv_id, data in queries.items():
            cv_emb = data["embedding"]
            cv_skills = data["skills"]

            results = self.client.query_points(
                collection_name=self.collection_name,
                query=cv_emb,
                limit=QDRANT_CANDIDATE_LIMIT,
            )

            scored = []
            for point in results.points:
                payload = point.payload or {}
                job_id = self._clean_job_id(payload.get("job_id", ""))
                job_skills = set(payload.get("skills", []))

                cosine = getattr(point, "score", 0.0)
                jac    = self.jaccard(cv_skills, job_skills)
                ov     = self.overlap(cv_skills, job_skills)

                final_score = ALPHA * cosine + BETA * jac + GAMMA * ov
                scored.append((job_id, round(final_score, 4)))

            scored.sort(key=lambda x: x[1], reverse=True)
            top = scored[:TOP_N_RESULTS]

            results_dict[cv_id] = {
                "job_ids": [j for j, _ in top],
                "scores":  top,
            }

        return results_dict

    def recommend(self, queries: dict) -> dict:
        """
        Pure vector search — no skill re-ranking.
        Faster but less accurate than recommend_hybrid.
        """
        results_dict = {}

        for cv_id, data in queries.items():
            results = self.client.query_points(
                collection_name=self.collection_name,
                query=data["embedding"],
                limit=TOP_N_RESULTS,
            )

            results_dict[cv_id] = {
                "job_ids": [
                    self._clean_job_id((p.payload or {}).get("job_id", ""))
                    for p in results.points
                ]
            }

        return results_dict