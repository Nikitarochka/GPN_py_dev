from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from statistics import median
from typing import List, Optional

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = models.Device(
        device_id=device.device_id,
        user_id=device.user_id
    )
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_device(db: Session, device_id: str):
    return db.query(models.Device).filter(models.Device.device_id == device_id).first()

def get_devices_by_user(db: Session, user_id: int) -> List[models.Device]:
    return db.query(models.Device).filter(models.Device.user_id == user_id).all()

def create_measurement(db: Session, measurement: models.Measurement):
    db.add(measurement)
    db.commit()
    db.refresh(measurement)
    return measurement

def get_measurements(db: Session, device_id: Optional[str] = None,
                     start: Optional[datetime] = None, end: Optional[datetime] = None) -> List[models.Measurement]:
    query = db.query(models.Measurement)
    if device_id:
        query = query.filter(models.Measurement.device_id == device_id)
    if start:
        query = query.filter(models.Measurement.timestamp >= start)
    if end:
        query = query.filter(models.Measurement.timestamp <= end)
    return query.all()

def analyze_measurements(measurements: List[models.Measurement]):
    x_values = [m.x for m in measurements]
    y_values = [m.y for m in measurements]
    z_values = [m.z for m in measurements]
    analysis = {
        "min": {
            "x": min(x_values),
            "y": min(y_values),
            "z": min(z_values)
        },
        "max": {
            "x": max(x_values),
            "y": max(y_values),
            "z": max(z_values)
        },
        "count": len(measurements),
        "sum": {
            "x": sum(x_values),
            "y": sum(y_values),
            "z": sum(z_values)
        },
        "median": {
            "x": median(x_values),
            "y": median(y_values),
            "z": median(z_values)
        }
    }
    return analysis
