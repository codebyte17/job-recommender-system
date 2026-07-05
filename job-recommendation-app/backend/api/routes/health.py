from fastapi import APIRouter
from db.mongodb import db
router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/health/db")
async def health_db():
    try:
        db.command("ping")
        return {"status": "ok", "mongodb": "connected"}
    except Exception as e:
        return {"status": "degraded", "mongodb": str(e)}