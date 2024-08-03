from fastapi import APIRouter, Body, Depends, HTTPException
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.api.dependencies.db import get_db
from app.schemas.station import Station as StationWithMetrics
from app.schemas.metric import Metric, MetricUpdate, MetricsRequestModel
from app.services.station_service import StationService
from datetime import datetime


router = APIRouter()


@router.post("", response_model=List[StationWithMetrics], responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "example":
                [
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
                                "created_at": "2024-08-03T11:51:28.082919",
                                "updated_at": "2024-08-03T11:51:28.082919",
                                "id": 4
                            },
                            {
                                "temperature": 10,
                                "humidity": 83,
                                "wind_speed": 2,
                                "wind_direction": "NE",
                                "precipitation": 12,
                                "created_at": "2024-08-03T12:08:01.782195",
                                "updated_at": "2024-08-03T12:08:01.782195",
                                "id": 6
                            }
                        ]
                    },
                    {
                        "name": "Sample Weather Station",
                        "longitude": -122.4194,
                        "latitude": 37.7749,
                        "is_active": True,
                        "id": 4,
                        "created_at": "2024-08-03T11:54:24.474724",
                        "updated_at": "2024-08-03T11:54:24.474724",
                        "metrics": [
                            {
                                "temperature": 11,
                                "humidity": 83,
                                "wind_speed": 2,
                                "wind_direction": "E",
                                "precipitation": 1,
                                "created_at": "2024-08-03T12:00:33.085028",
                                "updated_at": "2024-08-03T12:03:55.036432",
                                "id": 5
                            }
                        ]
                    }
                ],
            }
        }
    }
})
def get_metrics(
    request_body: MetricsRequestModel = Body(example={
        "start_date": "2024-08-03T12:42:18",
        "end_date": "2024-08-03T12:42:18",
        "station_ids": {
                    "station_ids": [1, 2, 4]
        }
    }, description="Request body containing filter parameters."),
    db: Session = Depends(get_db)
):
    """
    Despite being a POST request, this method is used to fetch metrics data.

    - **start_date**: Optional start date for filtering metrics.
    - **end_date**: Optional end date for filtering metrics.
    - **station_ids**: Optional dictionary containing a list of station IDs to filter metrics.

    In order to get full results an empty json '{}' must be passed as request body
    """

    metrics = StationService.get_metrics(
        db=db,
        start_date=request_body.start_date,
        end_date=request_body.end_date,
        station_ids=request_body.station_ids
    )

    if not metrics:
        raise HTTPException(status_code=404, detail="Metrics not found")

    return metrics
