from celery import Celery
from config import settings

celery_app = Celery(
    "job_recommender",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["tasks.recommendation"],   # auto-discovers the task module
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    task_track_started=True,            # enables "processing" state
    result_expires=3600,                # results live in Redis for 1 hour
    worker_prefetch_multiplier=1,       # one task at a time per worker
)

# --------------------------------
#          Monitoring
# --------------------------------
from prometheus_client import Gauge

cv_queue_size = Gauge(
    "cv_queue_size",
    "Number of CV tasks waiting in queue"
)

cv_queue_size.set(len(celery_app.control.inspect().active() or {}))