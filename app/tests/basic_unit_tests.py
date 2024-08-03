import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from app.db.base import Base
from app.models.station import Station
from app.schemas.station import StationCreate, StationUpdate
from app.schemas.metric import MetricCreate
from app.services.station_service import StationService
import pytz

# Create an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
timezone = pytz.UTC

# Setup the database and create the tables
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def db_session():
    """Fixture to create a new database session for each test"""
    session = TestingSessionLocal()
    yield session
    session.close()


def test_create_station(db_session):
    station_data = StationCreate(
        name="Test Station", longitude=0.0, latitude=0.0, is_active=True)
    station = StationService.create_station(db_session, station_data)
    assert station.id is not None
    assert station.name == "Test Station"


def test_get_stations(db_session):
    stations = StationService.get_stations(db_session)
    assert len(stations) > 0


def test_get_station_by_id(db_session):
    station = StationService.get_station_by_id(db_session, 1)
    assert station is not None
    assert station.id == 1


def test_update_station(db_session):
    station = StationService.get_station_by_id(db_session, 1)
    update_data = StationUpdate(
        name="Updated Station", longitude=1.0, latitude=1.0, is_active=False)
    updated_station = StationService.update_station(
        db_session, station, update_data)
    assert updated_station.name == "Updated Station"
    assert updated_station.longitude == 1.0
    assert updated_station.latitude == 1.0
    assert not updated_station.is_active


def test_delete_station(db_session):
    station = StationService.get_station_by_id(db_session, 1)
    StationService.delete_station(db_session, station)
    deleted_station = StationService.get_station_by_id(db_session, 1)
    assert deleted_station is None


def test_create_metric(db_session):
    # Create a station first
    station = Station(name="Test Station", longitude=0.0,
                      latitude=0.0, is_active=True)
    db_session.add(station)
    db_session.commit()
    db_session.refresh(station)

    metric_data = MetricCreate(
        temperature=22.0,
        humidity=45.0,
        wind_speed=5.0,
        wind_direction="N",
        precipitation=0.0
    )
    metric = StationService.create_metric(db_session, metric_data, station.id)

    assert metric is not None
    assert metric.temperature == 22.0
    assert metric.station_id == station.id


def test_get_metrics_for_station(db_session):
    station = StationService.get_stations(db_session)[0]
    metrics = StationService.get_metrics_for_station(station.id, db_session)
    assert metrics is not None


def test_get_metric_by_id(db_session):
    metric = StationService.get_metric_by_id(db_session, 1)
    assert metric is not None
    assert metric.id == 1


# Create a station and metric with timezone-aware datetime
def test_get_metric_by_date(db_session):
    # Create a station
    station = StationService.create_station(
        db_session, StationCreate(
            name="Test Station", longitude=0.0, latitude=0.0, is_active=True)
    )
    db_session.commit()
    db_session.refresh(station)

    # Create a metric
    created_at = datetime.now(timezone)  # Use timezone-aware datetime
    metric = StationService.create_metric(
        db_session, MetricCreate(
            temperature=25.0,
            humidity=60.0,
            wind_speed=10.0,
            wind_direction="N",
            precipitation=5.0
        ), station_id=station.id
    )
    metric.created_at = created_at
    db_session.commit()
    db_session.refresh(metric)

    # Print statements for debugging
    created_at_str = metric.created_at.strftime('%Y-%m-%d %H:%M:%S.%f %Z')
    print(f"Metric created at: {created_at_str}")

    # Fetch the metric by date
    fetched_metric = StationService.get_metric_by_date(
        db_session, station.id, created_at
    )

    # Print fetched metric for debugging
    if fetched_metric:
        fetched_created_at_str = fetched_metric.created_at.strftime(
            '%Y-%m-%d %H:%M:%S.%f %Z')
        print(f"Fetched metric created at: {fetched_created_at_str}")
    else:
        print("No metric fetched.")

    # Check if the fetched metric matches the created metric
    assert fetched_metric is not None, "Expected metric to be found in the database"
    assert fetched_metric.id == metric.id, "Fetched metric ID does not match the created metric ID"
    assert fetched_metric.temperature == metric.temperature
    assert fetched_metric.humidity == metric.humidity
    assert fetched_metric.wind_speed == metric.wind_speed
    assert fetched_metric.wind_direction == metric.wind_direction
    assert fetched_metric.precipitation == metric.precipitation


def test_get_metrics(db_session):
    start_date = datetime.utcnow() - timedelta(days=2)
    end_date = datetime.utcnow() + timedelta(days=2)
    stations = StationService.get_metrics(
        db_session, start_date=start_date, end_date=end_date)
    assert len(stations) > 0
