from sqlalchemy.orm import Session
import models


def get_flights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Flight).offset(skip).limit(limit).all()
