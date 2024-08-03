from typing import List, Optional
from fastapi import Depends, HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from app.models.station import Station, Metric
from app.schemas.station import StationCreate, StationUpdate
from app.schemas.metric import MetricCreate, StationIdsModel
from datetime import datetime, timedelta


class StationService:
    @staticmethod
    def get_stations(db: Session):
        return db.query(Station).all()

    @staticmethod
    def get_station_by_id(db: Session, station_id: int):
        return db.query(Station).filter(Station.id == station_id).first()

    @staticmethod
    def create_station(db: Session, station: StationCreate):
        db_item = Station(**station.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    @staticmethod
    def update_station(db: Session, station: Station, station_update: StationUpdate):
        # Exclude fields that were not set in the update request
        update_data = station_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(station, key, value)
        db.commit()
        db.refresh(station)
        return station

    @staticmethod
    def delete_station(db: Session, station: Station):
        db.delete(station)
        db.commit()

    @staticmethod
    def create_metric(db: Session, metric_data: MetricCreate, station_id: int):
        # Ensure station_id is valid
        station = db.query(Station).filter(Station.id == station_id).first()
        if not station:
            raise HTTPException(status_code=404, detail="Station not found")

        metric = Metric(temperature=metric_data.temperature,
                        humidity=metric_data.humidity,
                        wind_speed=metric_data.wind_speed,
                        wind_direction=metric_data.wind_direction,
                        precipitation=metric_data.precipitation,
                        station_id=station_id)
        db.add(metric)
        db.commit()
        db.refresh(metric)
        return metric

    @staticmethod
    def get_metrics_for_station(station_id: int, db: Session):
        return db.query(Station).filter(Station.id == station_id).first()

    @staticmethod
    def get_metric_by_id(db: Session, metric_id: int):
        return db.query(Metric).filter(Metric.id == metric_id).first()

    @staticmethod
    def get_metric_by_date(db: Session, station_id: int, created_at: datetime):
        # Zero out microseconds
        created_at_no_microseconds = created_at.replace(microsecond=0)
        next_second = created_at_no_microseconds + timedelta(seconds=1)

        return db.query(Metric).filter(
            Metric.station_id == station_id,
            Metric.created_at >= created_at_no_microseconds,
            Metric.created_at < next_second
        ).first()

    @staticmethod
    def get_metrics(db: Session,
                    start_date: Optional[datetime] = None,
                    end_date: Optional[datetime] = None,
                    station_ids: Optional[StationIdsModel] = None):

        # Convert StationIDsModel to list of IDs if provided
        if station_ids:
            station_ids_list = station_ids.station_ids
        else:
            station_ids_list = None

        # Query to get all stations with their metrics
        query = db.query(Station).options(joinedload(Station.metrics))

        # Filter by station IDs if provided
        if station_ids_list:
            query = query.filter(Station.id.in_(station_ids_list))

        # Execute the query
        stations = query.all()

        # Adjust start_date and end_date
        if start_date:
            start_date = start_date.replace(microsecond=0)
        if end_date:
            # Make end_date exclusive
            end_date = end_date.replace(microsecond=0) + timedelta(seconds=1)

        filtered_stations = []
        for station in stations:
            # Filter metrics based on the provided start_date and end_date
            filtered_metrics = [
                metric for metric in station.metrics
                if (start_date is None or metric.created_at >= start_date) and
                   (end_date is None or metric.created_at < end_date)
            ]
            if filtered_metrics:
                station.metrics = filtered_metrics
                filtered_stations.append(station)

        # Raise an exception if no stations match the filters
        if not filtered_stations:
            raise HTTPException(
                status_code=404, detail="No stations found with the given filters."
            )

        return filtered_stations
