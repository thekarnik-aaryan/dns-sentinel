from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import models, schemas

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

@router.get("", response_model=List[schemas.AlertRead])
def get_alerts(limit: int = Query(100), db: Session = Depends(get_db)):
    return db.query(models.Alert).order_by(models.Alert.timestamp.desc()).limit(limit).all()
