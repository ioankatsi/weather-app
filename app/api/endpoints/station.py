from fastapi import APIRouter, Depends, Body, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.api.dependencies.db import get_db
from datetime import datetime
from app.schemas.station import Station as StationWithMetrics, StationInfo, StationCreate, StationUpdate
from app.schemas.metric import Metric, MetricCreate, MetricUpdate
from app.services.station_service import StationService
from app.api.dependencies.auth import get_current_user
from app.schemas.user import TokenData
from app.core.log_conf import logging

api_logger = logging.getLogger("app")

router = APIRouter()


@router.post("/", response_model=StationInfo, summary="Create new weather station", description="Create a new entry in the database for a weather station", tags=["Stations"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "name": "Sample Weather Station",
                    "longitude": -122.4194,
                    "latitude": 37.7749,
                    "is_active": True,
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                }
            }
        }
    }
})
def create_station(station: StationCreate = Body(
    example={
        "name": "Sample Weather Station",
                "longitude": -122.4194,
                "latitude": 37.7749,
                "is_active": True
    }
), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return StationService.create_station(db=db, station=station)


@router.get("/", response_model=List[StationInfo], summary="Retrieve all weather stations", description="Get a list of all available weather stations from the database.", tags=["Stations"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example": [{
                    "id": 1,
                    "name": "Sample Weather Station",
                    "longitude": -122.4194,
                    "latitude": 37.7749,
                    "is_active": True,
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                },
                    {
                    "id": 2,
                    "name": "Sample Weather Station 2",
                    "longitude": -91.1312,
                    "latitude": 12.1313,
                    "is_active": True,
                    "created_at": "2024-05-03T00:00:00",
                    "updated_at": "2024-04-04T00:00:00"
                },
                ]
            }
        }
    }
})
def get_station(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Retrieve all weather stations.

    This endpoint retrieves all weather stations available in the database.

    - **db**: A database session dependency.
    """
    station = StationService.get_stations(db=db)
    return station


@router.get("/{station_id}", response_model=StationInfo, summary="Retrieve specific weather stations", description="Get a specific weather stations from the database based on unique ID .", tags=["Stations"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example":
                    {
                        "id": 2,
                        "name": "Sample Weather Station 2",
                        "longitude": -91.1312,
                        "latitude": 12.1313,
                        "is_active": True,
                        "created_at": "2024-05-03T00:00:00",
                        "updated_at": "2024-04-04T00:00:00"
                    },
            }
        }
    }
})
def get_station(station_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Create weather stations.
    """
    station = StationService.get_station_by_id(db=db, station_id=station_id)
    if station is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return station


@router.put("/{station_id}", response_model=StationInfo, summary="Update a station's information", description="Update the information of a specific station by its ID. If the station does not exist, a 404 error is returned.", tags=["Stations"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example":
                    {
                        "name": "Sample Weather Station New Name",
                        "longitude": -10.4194,
                        "latitude": 37.7749,
                        "is_active": False,
                        "id": 2,
                        "created_at": "2024-08-03T11:31:54.128656",
                        "updated_at": "2024-08-03T11:39:56.704229"
                    },
            }
        }
    }
})
def update_station(station_id: int, station_update: StationUpdate = Body(
        example={
            "name": "Sample Weather Station New Name",
            "longitude": -10.4194,
            "is_active": False
        }), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
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


@router.delete("/{station_id}", summary="Delete a specific station by ID", description="Delete a specific station by its ID. If the station does not exist, a 404 error is returned.", tags=["Stations"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example":
                {
                    "detail": "Station deleted successfully"
                },
            }
        }
    }
})
def delete_station(station_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
                   ):
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


@ router.post("/{station_id}/metric", response_model=Metric, summary="Create new metric", description="Create a new entry in the database for a specific metric for a specific weather station", tags=["Metrics"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example":
                {
                    "temperature": 10,
                    "humidity": 83,
                    "wind_speed": 2,
                    "wind_direction": "NE",
                    "precipitation": 12,
                    "created_at": "2024-08-03T11:44:35.189428",
                    "updated_at": "2024-08-03T11:44:35.189428",
                    "id": 1
                },
            }
        }
    }
})
def create_metric(station_id: int, metric: MetricCreate = Body(
        example={
            "temperature": 10,
            "humidity": 83,
            "wind_speed": 2,
            "wind_direction": "NE",
            "precipitation": 12,
        }), db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    return StationService.create_metric(db=db, metric_data=metric, station_id=station_id)


@ router.get("/{station_id}/metrics", response_model=StationWithMetrics, summary="Retrieve all metrics for a specific station", description="Get a list of all available metrics from a specific station from the database.", tags=["Metrics"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example":
                {
                    "name": "Sample Weather Station New Name",
                    "longitude": -10.4194,
                    "latitude": 37.7749,
                    "is_active": True,
                    "id": 1,
                    "created_at": "2024-08-03T11:31:54.128656",
                    "updated_at": "2024-08-03T11:39:56.704229",
                    "metrics": [
                        {
                            "temperature": 10,
                            "humidity": 83,
                            "wind_speed": 2,
                            "wind_direction": "NE",
                            "precipitation": 12,
                            "created_at": "2024-08-03T11:46:40.570523",
                            "updated_at": "2024-08-03T11:46:40.570523",
                            "id": 2
                        },
                        {
                            "temperature": -1,
                            "humidity": 74,
                            "wind_speed": 10,
                            "wind_direction": "N",
                            "precipitation": 80,
                            "created_at": "2024-08-03T11:50:28.627333",
                            "updated_at": "2024-08-03T11:50:28.627333",
                            "id": 8
                        },
                        {
                            "temperature": 5,
                            "humidity": 69,
                            "wind_speed": 1,
                            "wind_direction": "NE",
                            "precipitation": 0,
                            "created_at": "2024-08-03T11:51:28.082919",
                            "updated_at": "2024-08-03T11:51:28.082919",
                            "id": 15
                        }
                    ]
                }
            }
        }
    }
})
def get_metric(station_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    stationMetrics = StationService.get_metrics_for_station(
        db=db, station_id=station_id)
    if stationMetrics is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return stationMetrics


@ router.put("{station_id}/metric", response_model=Metric, summary="Update the information of a specific metric by its ID. If the station or the metric does not exist, a 404 error is returned.", tags=["Metrics"], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example":
                {
                    "temperature": 26,
                    "humidity": 12,
                    "wind_speed": 3,
                    "wind_direction": "W",
                    "precipitation": 12,
                    "created_at": "2024-08-03T11:44:35.189428",
                    "updated_at": "2024-08-05T11:44:35.189428",
                    "id": 10
                },
            }
        }
    }
})
def update_metric(
    station_id: int,
    created_at: datetime,
    metric_update: MetricUpdate = Body(
        example={
            "temperature": 10,
            "humidity": 83,
            "wind_speed": 2,
            "wind_direction": "NE",
            "precipitation": 12,
        }),
    db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)
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
