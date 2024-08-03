from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MetricBase(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    wind_direction: str
    precipitation: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MetricCreate(MetricBase):
    pass


class Metric(MetricBase):
    id: int

    class Config:
        from_attributes = True


class MetricUpdate(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_direction: Optional[str] = None
    precipitation: Optional[float] = None
