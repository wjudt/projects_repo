import datetime

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import read, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/flights/", response_model=list[schemas.FlightBase])
def read_flights(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    flights = read.get_flights(db, skip=skip, limit=limit)
    return flights


@app.get("/flight/icao24={icao}", response_model=schemas.FlightBase)
def read_flight_by_icao(icao: str, db: Session = Depends(get_db)):
    flight_by_icao = read.get_flight_by_icao(db, icao=icao.lower())
    if flight_by_icao is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight_by_icao


@app.get("/flights/startdate={start}enddate={end}", response_model=list[schemas.FlightBase])
def read_flights_by_date(start: str, end: str, db: Session = Depends(get_db)):
    flights_by_date = read.get_flights_by_date(db,
                                               start_date=datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S"),
                                               end_date=datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S"))
    if flights_by_date is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flights_by_date