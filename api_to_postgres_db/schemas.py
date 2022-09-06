import datetime

from pydantic import BaseModel


class FlightBase(BaseModel):
    icao24: str
    callsign: str | None = None
    origin_country: str
    time_position: datetime.datetime | None = None
    time_last_contact: datetime.datetime | None = None
    longitude_deg: float | None = None
    latitude_deg: float | None = None
    geo_altitude_m: float | None = None
    on_ground: bool | None = None
    velocity_m_per_s: float | None = None
    true_track_dec_deg: float | None = None
    vertical_rate_m_per_s: float | None = None
    sensors: str | None = None
    baro_altitude_m: float | None = None
    squawk_code: int
    spi: bool
    position_source: int | None = None
    dag_utc_time_str: datetime.datetime

    class Config:
        orm_mode = True
