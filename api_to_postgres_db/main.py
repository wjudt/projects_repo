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


