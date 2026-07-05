from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from config import settings

from api.routes import cv_router,health_router





app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

Instrumentator().instrument(app).expose(app)
app.include_router(health_router)
app.include_router(cv_router)