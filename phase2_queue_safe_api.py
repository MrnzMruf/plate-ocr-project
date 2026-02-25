# phase2_queue_safe_api.py
# Phase 2: Added Redis + Celery queue + unlimited retry
# Goal: Zero data loss even if worker crashes or network issues
# max_retries=None was the key change

from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from celery import Celery
import uuid

app = FastAPI(title="Phase 2 - Queue Safe API")

# Celery setup - Redis as broker & result backend
celery = Celery(
    "anpr_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Task with unlimited retries for zero data loss
@celery.task(bind=True, max_retries=None, default_retry_delay=5)
def process_image(self, task_id, filename):
    # Simulate heavy work (OCR / plate detection)
    # In production this would be the real processing
    try:
        print(f"[{task_id}] Processing {filename}")
        # ... real OCR code would be here ...
        return {"plate": "۱۲ الف ۳۴۵", "confidence": 0.95}
    except Exception as exc:
        raise self.retry(exc=exc)  # retry forever until success

@app.post("/upload/")
def upload(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    task_id = str(uuid.uuid4())
    
    # Queue the task instead of processing immediately
    background_tasks.add_task(
        process_image.delay,
        task_id=task_id,
        filename=file.filename
    )
    
    return {"status": "queued", "task_id": task_id}
