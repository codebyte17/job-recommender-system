import numpy as np
from config_engine import SKILL_SCORE_THRESHOLD


class QueryPreparer:
    """
    Prepares a single CV text into a query dict
    the RecommendationEngine can consume.
    """

    def __init__(self, model, skill_extractor, skill_db):
        self.model = model
        self.skill_extractor = skill_extractor
        self.skill_db = skill_db

    def extract_skills(self, text: str) -> set:
        try:
            annotations = self.skill_extractor.annotate(text)
            skills = set()

            for s in annotations["results"].get("full_matches", []):
                skill_name = self.skill_db[s["skill_id"]]["skill_name"]
                skills.add(skill_name)

            for s in annotations["results"].get("ngram_scored", []):
                if s["score"] > SKILL_SCORE_THRESHOLD:
                    skill_name = self.skill_db[s["skill_id"]]["skill_name"]
                    skills.add(skill_name)

            return skills

        except Exception as e:
            print(f"[QueryPreparer] skill extraction failed: {e}")
            return set()

    def get_embedding(self, text: str) -> np.ndarray:
        return self.model.encode(text)

    def prepare_single(self, cv_id: str, cv_text: str) -> dict:
        """
        Prepares one CV into a query dict.

        Returns:
            {
                cv_id: {
                    "skills": set(),
                    "embedding": np.ndarray
                }
            }
        """
        return {
            cv_id: {
                "skills": self.extract_skills(cv_text),
                "embedding": self.get_embedding(cv_text),
            }
        }

    def build_queries(self, df, cv_count: int) -> dict:
        """
        Batch version — kept for compatibility with your existing code.
        Processes multiple CVs from a DataFrame.

        Returns:
            {
                cv_id: {
                    "skills": set(),
                    "embedding": np.ndarray
                }
            }
        """
        df = df.iloc[:cv_count]
        queries = {}
        for _, row in df.iterrows():
            cv_id = row["job_id"]
            text = row["cvs"]
            queries[cv_id] = {
                "skills": self.extract_skills(text),
                "embedding": self.get_embedding(text),
            }
        return queries