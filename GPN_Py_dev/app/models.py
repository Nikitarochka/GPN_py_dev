from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    devices = relationship("Device", back_populates="owner")

class Device(Base):
    __tablename__ = "devices"
    device_id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="devices")
    measurements = relationship("Measurement", back_populates="device")

class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.device_id"), nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)
    device = relationship("Device", back_populates="measurements")
