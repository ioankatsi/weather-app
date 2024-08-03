from typing import List, Optional
from fastapi import Depends, HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from app.models.station import Station, Metric
from app.schemas.station import StationCreate, StationUpdate
from app.schemas.metric import MetricCreate, StationIdsModel
from datetime import datetime, timedelta
from app.core.log_conf import logging

api_logger = logging.getLogger("app")


class StationService:
    @staticmethod
    def get_stations(db: Session):
        try:
            return db.query(Station).all()
        except Exception as e:
            api_logger.error(
                'Unable to fetch stations, error: %s' % e)

    @staticmethod
    def get_station_by_id(db: Session, station_id: int):
        try:
            return db.query(Station).filter(Station.id == station_id).first()
        except Exception as e:
            api_logger.error(
                'Unable to fetch station, error: %s' % e)

    @staticmethod
    def create_station(db: Session, station: StationCreate):
        try:
            db_item = Station(**station.dict())
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            return db_item
        except Exception as e:
            api_logger.error(
                'Unable to store station, error: %s' % e)

    @staticmethod
    def update_station(db: Session, station: Station, station_update: StationUpdate):
        try:
            # Exclude fields that were not set in the update request
            update_data = station_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(station, key, value)
            db.commit()
            db.refresh(station)
            return station
        except Exception as e:
            api_logger.error(
                'Unable to update station, error: %s' % e)

    @staticmethod
    def delete_station(db: Session, station: Station):
        try:
            db.delete(station)
            db.commit()
        except Exception as e:
            api_logger.error(
                'Unable to delete station, error: %s' % e)

    @staticmethod
    def create_metric(db: Session, metric_data: MetricCreate, station_id: int):
        # Ensure station_id is valid
        station = db.query(Station).filter(Station.id == station_id).first()
        if not station:
            api_logger.warning('Unable to get station')
            raise HTTPException(status_code=404, detail="Station not found")

        try:
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
        except Exception as e:
            api_logger.error(
                'Unable to store metric, error: %s' % e)

    @staticmethod
    def get_metrics_for_station(station_id: int, db: Session):
        try:
            return db.query(Station).filter(Station.id == station_id).first()
        except Exception as e:
            api_logger.error(
                'Unable to get metric for station, error: %s' % e)

    @staticmethod
    def get_metric_by_id(db: Session, metric_id: int):
        try:
            return db.query(Metric).filter(Metric.id == metric_id).first()
        except Exception as e:
            api_logger.error(
                'Unable to get metric by id, error: %s' % e)

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
        try:
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
                end_date = end_date.replace(
                    microsecond=0) + timedelta(seconds=1)

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
        except Exception as e:
            api_logger.error(
                'Unable to get metrics: %s' % e)
