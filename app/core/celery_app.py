import os
from celery import Celery

celery = Celery(
    "Pdf processor",
    broker=os.getenv(
        "CELERY_BROKER_URL", "redis://localhost:6379/0"
    ),  # Broker for handling tasks (Redis)
    backend=os.getenv(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
    ),  # Backend for storing task results (Redis)
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    include=["app.tasks"],
)
