from fastapi import APIRouter , UploadFile, File, HTTPException
from celery.result import AsyncResult

from models.cv import CVUploadResponse, TaskStatusResponse
from config import settings
from tasks.recommendation import process_cv
from core.celery_app import celery_app

# ----------------------------------------------
#              Monitoring
# ----------------------------------------------
from prometheus_client import Counter

cv_upload_total = Counter(
    "cv_upload_total",
    "Total number of CV uploads"
)
cv_upload_invalid_total = Counter(
    "cv_upload_invalid_total",
    "Invalid CV uploads (wrong format, empty, etc.)"
)

cv_processing_success_total = Counter(
    "cv_processing_success_total",
    "Successfully processed CVs"
)

cv_processing_failure_total = Counter(
    "cv_processing_failure_total",
    "Failed CV processing jobs"
)

jobs_recommended_total = Counter(
    "jobs_recommended_total",
    "Total job recommendations generated"
)


router = APIRouter(prefix="/api", tags=["cv"])
@router.post("/upload-cv", response_model=CVUploadResponse)
async def upload_cv(file: UploadFile = File(...)):
    cv_upload_total.inc()  # monitor the uploaded cvs
    if not file.filename.endswith(".txt"):
        cv_upload_invalid_total.inc()
        raise HTTPException(status_code=400, detail="Invalid file type : Only .txt files supported")

    content = await file.read()
    if len(content) > settings.max_cv_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Max size: {settings.max_cv_size_bytes // 1000} KB",
        )

    cv_text = content.decode("utf-8", errors="ignore")
    if not cv_text.strip():
        raise HTTPException(status_code=400, detail="CV file is empty")

    # Enqueue the Celery task — returns immediately with a task_id
    task = process_cv.delay(str(cv_text))

    return CVUploadResponse(task_id=task.id)



@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    try:
        state = result.state
    except Exception:
        return {
            "task_id": task_id,
            "status": "unknown",
            "jobs": [],
            "error": "Corrupted Celery result in Redis"
        }

    if state == "PENDING":
        return TaskStatusResponse(
            task_id=task_id,
                status="pending",
                jobs=[],
                error=None
            )

    if state == "STARTED":
        return TaskStatusResponse(
                task_id=task_id,
                status="processing",
                jobs=[],
                error=None
            )

    if state == "SUCCESS":
        data = result.result or {}
        jobs_recommended_total.inc(len(data.get("jobs", [])))
        cv_processing_success_total.inc()
        return TaskStatusResponse(
                task_id=task_id,
                status="done",
                jobs=data.get("jobs", []) if isinstance(data, dict) else [],
                error=None
            )

    if state == "FAILURE":
        cv_processing_failure_total.inc()
        return TaskStatusResponse(
                task_id=task_id,
                status="failed",
                jobs=[],
                error=str(result.info)
            )

    return TaskStatusResponse(
            task_id=task_id,
            status=state.lower(),
            jobs=[],
            error=None
        )