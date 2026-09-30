import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field

class DNSQueryBase(BaseModel):
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    source_ip: str
    destination_ip: str
    query_name: str
    query_type: str = "A"
    response_code: str = "NOERROR"
    packet_size: int = 0

class DNSQueryRead(DNSQueryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class AlertRead(BaseModel):
    id: int
    timestamp: datetime.datetime
    detector: str
    severity: str
    risk_score: float
    confidence: float
    title: str
    description: str
    evidence: str
    mitre_technique: Optional[str] = None
    status: str
    model_config = ConfigDict(from_attributes=True)

class DashboardSummary(BaseModel):
    total_queries: int
    suspicious_queries: int
    active_alerts: int
    critical_alerts: int
    query_rate_per_min: float
