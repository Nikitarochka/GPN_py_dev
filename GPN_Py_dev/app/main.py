from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, crud, tasks, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Сервис учета и анализа данных")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Healthcheck endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
    return crud.create_user(db, user)

@app.post("/devices", response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=device.user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db_device = crud.get_device(db, device_id=device.device_id)
    if db_device:
        raise HTTPException(status_code=400, detail="Устройство с таким ID уже существует")
    return crud.create_device(db, device)

@app.post("/measurements")
def create_measurement(measurement: schemas.MeasurementCreate, db: Session = Depends(get_db)):
    db_device = crud.get_device(db, device_id=measurement.device_id)
    if not db_device:
        raise HTTPException(status_code=404, detail="Устройство не найдено. Сначала создайте устройство.")
    new_measurement = models.Measurement(
        device_id=measurement.device_id,
        timestamp=measurement.timestamp,
        x=measurement.data.get("x"),
        y=measurement.data.get("y"),
        z=measurement.data.get("z")
    )
    crud.create_measurement(db, new_measurement)
    return {"message": "Измерение успешно сохранено"}

@app.get("/analysis", response_model=schemas.AnalysisResult)
def get_analysis(device_id: str = None, start: datetime = None, end: datetime = None, db: Session = Depends(get_db)):
    measurements = crud.get_measurements(db, device_id=device_id, start=start, end=end)
    if not measurements:
        raise HTTPException(status_code=404, detail="Измерения не найдены")
    analysis = crud.analyze_measurements(measurements)
    return analysis

@app.get("/analysis/user/{user_id}", response_model=schemas.UserAnalysisResult)
def get_user_analysis(user_id: int, start: datetime = None, end: datetime = None, db: Session = Depends(get_db)):
    devices = crud.get_devices_by_user(db, user_id=user_id)
    if not devices:
        raise HTTPException(status_code=404, detail="Устройства пользователя не найдены")
    aggregated_measurements = []
    per_device_analysis = {}
    for device in devices:
        measurements = crud.get_measurements(db, device_id=device.device_id, start=start, end=end)
        if measurements:
            aggregated_measurements.extend(measurements)
            per_device_analysis[device.device_id] = crud.analyze_measurements(measurements)
    if not aggregated_measurements:
        raise HTTPException(status_code=404, detail="Измерения не найдены для устройств пользователя")
    aggregated_analysis = crud.analyze_measurements(aggregated_measurements)
    return schemas.UserAnalysisResult(
        aggregated=aggregated_analysis,
        per_device=per_device_analysis
    )

@app.get("/analysis/async")
def async_analysis(device_id: str = None, start: str = None, end: str = None):
    task = tasks.async_analysis.delay(device_id=device_id, start=start, end=end)
    return {"task_id": task.id, "status": "Запущено"}
