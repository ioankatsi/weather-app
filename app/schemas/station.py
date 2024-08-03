from pydantic import BaseModel, confloat
from datetime import datetime
from typing import List, Optional
from .metric import Metric


class StationBase(BaseModel):
    name: str
    longitude: Optional[confloat(ge=-180.0, le=180.0)] = None
    latitude: Optional[confloat(ge=-90.0, le=90.0)] = None
    is_active: bool

    class Config:
        from_attributes = True


class StationInfo(StationBase):
    id: int
    created_at: datetime
    updated_at: datetime


class StationCreate(StationBase):
    pass

    class Config:
        from_attributes = True

        json_schema_extra = {
            "example": {
                "name": "Sample Weather Station",
                "longitude": -122.4194,
                "latitude": 37.7749,
                "is_active": True
            }
        }


class Station(StationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    metrics: Optional[List['Metric']] = []

    class Config:
        from_attributes = True


class StationUpdate(BaseModel):
    name: Optional[str] = None
    longitude: Optional[confloat(ge=-180.0, le=180.0)] = None
    latitude: Optional[confloat(ge=-90.0, le=90.0)] = None
    is_active: Optional[bool] = None


class StationWithMetrics(BaseModel):
    station: Station
    metrics: List[Metric]

    class Config:
        from_attributes = True
