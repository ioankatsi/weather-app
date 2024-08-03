from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from app.api.dependencies.db import get_db
from app.schemas.station import Station as StationWithMetrics
from app.schemas.metric import Metric, MetricUpdate
from app.services.station_service import StationService
from datetime import datetime


router = APIRouter()


@router.post("", response_model=List[StationWithMetrics])
def get_metrics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    station_ids: Optional[List[int]] = None,
    db: Session = Depends(get_db)
):
    """
    Despite being a post, this method is used to fetch metrics data
    """
    metrics = StationService.get_metrics(
        db=db, start_date=start_date, end_date=end_date, station_ids=station_ids)

    if not metrics:
        raise HTTPException(status_code=404, detail="Metrics not found")

    return metrics
