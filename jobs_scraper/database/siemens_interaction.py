from datetime import datetime
from . import db
from pymongo import UpdateOne

class SiemensDB:
    def __init__(self):
        self.collector_collection = db["jobs_ids"]
        self.extractor_collection = db["jobs_details"]
    def save_job_to_mongodb(self, jobs):
        """
        Save multiple job IDs from dictionary into MongoDB at once
        jobs format:
        {
            0: '501215',
            1: '502568'
        }
        """

        operations = []

        for _, job_id in jobs.items():
            document = {
                "job_id": job_id,
                "source": "Siemens",
                "status": "pending",
                "scraped_at": datetime.utcnow()
            }

            operations.append(
                UpdateOne(
                    {"job_id": job_id},  # Check existing
                    {"$setOnInsert": document},  # Insert only if new
                    upsert=True
                )
            )

        if operations:
            result = self.collector_collection.bulk_write(operations)

            print(f"Inserted: {result.upserted_count}")
            print(f"Already existed / skipped: {len(jobs) - result.upserted_count}")

    def load_jobs_ids_from_mongodb(self):
        #jobs = {0: '501215', 1: '502568', 2: '503369', 3: '503989', 4: '504163', 5: '504182'}
        jobs = self.collector_collection.find({"status": "pending"})
        jobs = [job["job_id"] for job in jobs]
        return jobs

    def insert_jobs_details(self,job):
        self.extractor_collection.insert_one(self.normalize_job(job))

    def update_jobs_id_status(self,job_id):
        result = self.collector_collection.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "status": "Completed",
                    "updated_at": datetime.utcnow()
                }
            }
        )

        if result.matched_count == 0:
            print(f"No document found for job_id: {job_id}")
        else:
            print(f"Updated job_id: {job_id} -> status: Completed")

    @staticmethod
    def normalize_job(raw: dict) -> dict:
        # Safe getter (keeps None if missing)
        def get(key):
            return raw.get(key, None)

        # Handle location variants
        location = raw.get("location(s)", None) or raw.get("location", None)

        # Parse date safely, otherwise keep None
        posted_since = raw.get("posted_since", None)
        if posted_since:
            try:
                posted_since = datetime.strptime(posted_since, "%d-%b-%Y")
            except Exception as e:
                print(type(e).__name__,
                      e.__traceback__.tb_lineno,
                      "Posted_since is not a valid date or not Found!")
                posted_since = None

        doc = {
            "job_id": get("job_id"),
            "job_title": get("job_title"),
            "posted_since": posted_since,
            "organization": get("organization"),
            "field_of_work": get("field_of_work"),
            "company": get("company"),
            "experience_level": get("experience_level"),
            "job_type": get("job_type"),
            "work_mode": get("work_mode"),
            "employment_type": get("employment_type"),
            "location": location,
            "description": get("description"),
        }

        return doc

