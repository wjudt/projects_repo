from sqlalchemy import Boolean, Column, Integer, Float, String, DateTime
from sqlalchemy.schema import PrimaryKeyConstraint

from database import Base


class Flight(Base):
    __tablename__ = "area1_flat"

    icao24 = Column(String, primary_key=True)
    callsign = Column(String)
    origin_country = Column(String, nullable=False)
    time_position = Column(DateTime)
    time_last_contact = Column(DateTime, nullable=False)
    longitude_deg = Column(Float)
    latitude_deg = Column(Float)
    geo_altitude_m = Column(Float)
    on_ground = Column(Boolean, nullable=False)
    velocity_m_per_s = Column(Float)
    true_track_dec_deg = Column(Float)
    vertical_rate_m_per_s = Column(Float)
    sensors = Column(String)
    baro_altitude_m = Column(Float)
    squawk_code = Column(Integer)
    spi = Column(Boolean, nullable=False)
    position_source = Column(Integer)
    dag_utc_time_str = Column(DateTime, primary_key=True, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(icao24, dag_utc_time_str),
    )