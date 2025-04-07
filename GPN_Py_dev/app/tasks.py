from celery import Celery
from datetime import datetime
from .database import SessionLocal
from . import crud

celery = Celery("tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0")

@celery.task
def async_analysis(device_id: str = None, start: str = None, end: str = None):
    db = SessionLocal()
    start_dt = datetime.fromisoformat(start) if start else None
    end_dt = datetime.fromisoformat(end) if end else None
    measurements = crud.get_measurements(db, device_id=device_id, start=start_dt, end=end_dt)
    analysis = crud.analyze_measurements(measurements)
    db.close()
    return analysis
