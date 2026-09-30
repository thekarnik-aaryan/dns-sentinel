from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import models, schemas

router = APIRouter(prefix="/api", tags=["stats"])

@router.get("/dashboard/summary", response_model=schemas.DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)):
    total = db.query(models.DNSQuery).count()
    suspicious = db.query(models.Alert).count()
    active = db.query(models.Alert).filter(models.Alert.status == "NEW").count()
    critical = db.query(models.Alert).filter(models.Alert.severity == "CRITICAL").count()
    return schemas.DashboardSummary(
        total_queries=total, suspicious_queries=suspicious, active_alerts=active,
        critical_alerts=critical, query_rate_per_min=5.0
    )
