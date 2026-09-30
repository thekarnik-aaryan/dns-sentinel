from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import models, schemas

router = APIRouter(prefix="/api/dns", tags=["dns"])

@router.get("/recent", response_model=List[schemas.DNSQueryRead])
def get_recent_queries(limit: int = Query(50), db: Session = Depends(get_db)):
    return db.query(models.DNSQuery).order_by(models.DNSQuery.timestamp.desc()).limit(limit).all()
