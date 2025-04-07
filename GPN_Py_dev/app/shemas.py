from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class DeviceBase(BaseModel):
    device_id: str

class DeviceCreate(DeviceBase):
    user_id: int

class Device(DeviceBase):
    user_id: int
    class Config:
        orm_mode = True

class MeasurementBase(BaseModel):
    device_id: str
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    data: dict

class MeasurementCreate(MeasurementBase):
    pass

class AnalysisValue(BaseModel):
    x: float
    y: float
    z: float

class AnalysisResult(BaseModel):
    min: AnalysisValue
    max: AnalysisValue
    count: int
    sum: AnalysisValue
    median: AnalysisValue

class UserAnalysisResult(BaseModel):
    aggregated: AnalysisResult
    per_device: Dict[str, AnalysisResult]
