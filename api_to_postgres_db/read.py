import datetime

from sqlalchemy.orm import Session
from sqlalchemy import and_
import models


def get_flights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Flight).offset(skip).limit(limit).all()


def get_flight_by_icao(db: Session, icao: str):
    return db.query(models.Flight).filter(models.Flight.icao24 == icao).first()


def get_flights_by_date(db: Session,
                        start_date: datetime.datetime = datetime.datetime(2022, 8, 30, 9, 30),
                        end_date: datetime.datetime = datetime.datetime(2022, 8, 30, 9, 30)):
    return db.query(models.Flight).filter(and_(models.Flight.dag_utc_time_str >= start_date,
                                               end_date >= models.Flight.dag_utc_time_str)).all()

