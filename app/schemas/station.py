from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .metric import Metric


class StationBase(BaseModel):
    name: str
    longitude: float
    latitude: float
    is_active: bool

    class Config:
        from_attributes = True


class StationInfo(StationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StationCreate(StationBase):
    pass


class Station(StationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    metrics: Optional[List['Metric']] = []

    class Config:
        from_attributes = True


class StationUpdate(BaseModel):
    name: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    is_active: Optional[bool] = None


class StationWithMetrics(BaseModel):
    station: Station
    metrics: List[Metric]

    class Config:
        from_attributes = True
