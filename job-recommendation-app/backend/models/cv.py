from pydantic import BaseModel


class CVUploadResponse(BaseModel):
    task_id: str
    message: str = "CV submitted for processing"


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str          # pending | processing | done | failed
    jobs: list[dict] = []
    error: str | None = None