from sqlalchemy import BigInteger, Boolean, Column, Integer, DateTime, String, Float, ForeignKey
from sqlalchemy import TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    longitude = Column(Float, index=True)
    latitude = Column(Float, index=True)
    is_active = Column(Boolean, index=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)

    metrics = relationship("Metric", back_populates="station")


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, index=True)
    humidity = Column(Float, index=True)
    wind_speed = Column(Float, index=True)
    wind_direction = Column(String, index=True)
    precipitation = Column(Float, index=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)
    station_id = Column(Integer, ForeignKey('stations.id'), nullable=False)

    station = relationship("Station", back_populates="metrics")

    def as_dict(self):
        return {
            "id": self.id,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "wind_speed": self.wind_speed,
            "wind_direction": self.wind_direction,
            "precipitation": self.precipitation,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "station_id": self.station_id
        }
