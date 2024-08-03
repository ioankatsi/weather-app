from pydantic import BaseModel, confloat, validator
from datetime import datetime
from typing import Optional, List, Literal


class StationIdsModel(BaseModel):
    station_ids: List[int]


class MetricsRequestModel(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    station_ids: Optional[StationIdsModel] = None


class MetricBase(BaseModel):
    temperature: Optional[confloat(ge=-50.0, le=100.0)] = None
    humidity: Optional[confloat(ge=0, le=100.0)] = None
    wind_speed: Optional[confloat(ge=0, le=200.0)] = None
    wind_direction: Optional[Literal["N", "NE",
                                     "E", "SE", "S", "SW", "W", "NW"]] = None
    precipitation: Optional[confloat(ge=0, le=10000.0)] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MetricCreate(MetricBase):
    @validator('wind_direction', pre=True, always=True)
    def uppercase_wind_direction(cls, value):
        if value:
            return value.upper()
        return value

    class Config:
        from_attributes = True


class Metric(MetricBase):
    id: int

    class Config:
        from_attributes = True


class MetricUpdate(BaseModel):
    temperature: Optional[confloat(ge=-50.0, le=100.0)] = None
    humidity: Optional[confloat(ge=0, le=100.0)] = None
    wind_speed: Optional[confloat(ge=0, le=200.0)] = None
    wind_direction: Optional[Literal["N", "NE",
                                     "E", "SE", "S", "SW", "W", "NW"]] = None
    precipitation: Optional[confloat(ge=0, le=10000.0)] = None

    @validator('wind_direction', pre=True, always=True)
    def uppercase_wind_direction(cls, value):
        if value:
            return value.upper()
        return value
