from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.api.dependencies.db import get_db
from datetime import datetime
from app.schemas.station import Station as StationWithMetrics, StationInfo, StationCreate, StationUpdate
from app.schemas.metric import Metric, MetricCreate, MetricUpdate
from app.services.station_service import StationService
from app.api.dependencies.auth import get_current_user
from app.schemas.user import TokenData

router = APIRouter()


@router.post("/", response_model=StationInfo, summary="Create new weather station", description="Create a new entry in the database for a weather station", tags=["Stations"])
def create_station(station: StationCreate, db: Session = Depends(get_db)):
    return StationService.create_station(db=db, station=station)


@router.get("/", response_model=List[StationInfo], summary="Retrieve all weather stations", description="Get a list of all available weather stations from the database.", tags=["Stations"])
def get_station(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve all weather stations.

    This endpoint retrieves all weather stations available in the database.

    - **db**: A database session dependency.
    """
    station = StationService.get_stations(db=db)
    return station


@router.get("/{station_id}", response_model=StationInfo, summary="Retrieve specific weather stations", description="Get a specific weather stations from the database based on unique ID .", tags=["Stations"])
def get_station(station_id: int, db: Session = Depends(get_db)):
    """
    Create weather stations.
    """
    station = StationService.get_station_by_id(db=db, station_id=station_id)
    if station is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return station


@router.put("/{station_id}", response_model=StationInfo, summary="Update a station's information", description="Update the information of a specific station by its ID. If the station does not exist, a 404 error is returned.", tags=["Stations"])
def update_station(station_id: int, station_update: StationUpdate, db: Session = Depends(get_db)):
    """
    Update a station's information.

    This endpoint updates the information of a specific station using its unique ID.

    - **station_id**: The unique ID of the station.
    - **station_update**: The new data to update the station with.
    - **db**: A database session dependency.
    """
    station = StationService.get_station_by_id(db=db, station_id=station_id)
    if station is None:
        raise HTTPException(status_code=404, detail="Station not found")

    updated_station = StationService.update_station(
        db=db, station=station, station_update=station_update)
    return updated_station


@router.delete("/{station_id}", summary="Delete a specific station by ID", description="Delete a specific station by its ID. If the station does not exist, a 404 error is returned.", tags=["Stations"])
def delete_station(station_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific station by ID.

    This endpoint deletes a specific station using its unique ID.

    - **station_id**: The unique ID of the station.
    - **db**: A database session dependency.
    """
    station = StationService.get_station_by_id(db=db, station_id=station_id)
    if station is None:
        raise HTTPException(status_code=404, detail="Station not found")

    StationService.delete_station(db=db, station=station)
    return {"detail": "Station deleted successfully"}


@router.post("/{station_id}/metric", response_model=Metric, summary="Create new metric", description="Create a new entry in the database for a specific metric for a specific weather station", tags=["Metrics"])
def create_metric(station_id: int, metric: MetricCreate, db: Session = Depends(get_db)):
    return StationService.create_metric(db=db, metric_data=metric, station_id=station_id)


@router.get("/{station_id}/metrics", response_model=StationWithMetrics, summary="Retrieve all metrics for a specific station", description="Get a list of all available metrics from a specific station from the database.", tags=["Metrics"])
def get_metric(station_id: int, db: Session = Depends(get_db)):
    stationMetrics = StationService.get_metrics_for_station(
        db=db, station_id=station_id)
    if stationMetrics is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return stationMetrics


@router.put("{station_id}/metric", response_model=Metric, summary="Update the information of a specific metric by its ID. If the station or the metric does not exist, a 404 error is returned.", tags=["Metrics"])
def update_metric(
    station_id: int,
    created_at: datetime,
    metric_update: MetricUpdate,
    db: Session = Depends(get_db)
):
    station = StationService.get_station_by_id(db=db, station_id=station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")

    metric = StationService.get_metric_by_date(
        db=db, station_id=station_id, created_at=created_at)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")

    # Exclude fields that were not set in the update request
    update_data = metric_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(metric, key, value)
    # Ensure the `updated_at` field is updated
    metric.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(metric)
    return metric
