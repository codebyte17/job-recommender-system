from motor.motor_asyncio import AsyncIOMotorDatabase
from models.job import JobDocument

# ToDO: add it to async
def fetch_jobs_by_ids(
    db,
    job_ids: list[str],
    scores: dict[str, float],
) -> list[dict]:
    """
    Fetch job documents from MongoDB by their IDs,
    attach the recommendation score, and sort by score descending.
    """

    #job_ids = [str(jid) for jid in job_ids]
    cursor = db["jobs"].find(
        {"job_id": {"$in": job_ids}},
        {"_id": 0}  # remove ObjectId completely
    )
    jobs = []
    #ToDo: add async
    for doc in cursor:
        doc["score"] = scores.get(doc["job_id"], 0.0)
        jobs.append(doc)
    jobs.sort(key=lambda j: j["score"], reverse=True)
    return jobs

