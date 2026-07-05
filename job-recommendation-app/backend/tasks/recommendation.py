import asyncio
import os
import sys

# ── Bridge to recommendation-engine ───────────────────────────────────
ENGINE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "recommendation_engine",
)
sys.path.insert(0, ENGINE_PATH)

from engine import recommend_for_cv   # ← your engine's public function
#from recommendation_engine.engine import recommender_for_cv
# ──────────────────────────────────────────────────────────────────────

from core.celery_app import celery_app
from db.mongodb import db
from services.job_fetcher import fetch_jobs_by_ids


def _run_async(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(bind=True, name="tasks.recommendation.process_cv")
def process_cv(self,cv_text: str):
    try:
        # Step 1: load all job IDs from MongoDB
        self.update_state(state="STARTED", meta={"step": "running recommendation engine"})

        # Step 2: run recommendation engine
        result = recommend_for_cv(
            cv_text=cv_text,
            cv_id=self.request.id,   # use Celery task ID as CV identifier
            hybrid=True
        )

        # Step 3: fetch job details from MongoDB
        # ToDO: we need to change this once get the recommended jobs list
        score_map = dict(result.get("scores", []))
        jobs = fetch_jobs_by_ids(db, result["job_ids"], score_map)

        return {
            "status" : "success",
            "jobs": jobs
            }

    except Exception as exc:
        self.update_state(
            state="FAILURE",
            meta={"status": str(exc)},
        )
        raise