import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database.database import Base

class DNSQuery(Base):
    __tablename__ = "dns_queries"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True, nullable=False)
    source_ip = Column(String(45), index=True, nullable=False)
    destination_ip = Column(String(45), nullable=False)
    query_name = Column(String(255), index=True, nullable=False)
    query_type = Column(String(10), nullable=False, default="A")
    response_code = Column(String(20), nullable=False, default="NOERROR")
    packet_size = Column(Integer, nullable=False, default=0)
    response_time = Column(Float, nullable=True)

    features = relationship("DNSFeature", back_populates="query", uselist=False, cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="query", cascade="all, delete-orphan")

class DNSFeature(Base):
    __tablename__ = "dns_features"
    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("dns_queries.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    domain_length = Column(Integer, nullable=False)
    subdomain_length = Column(Integer, nullable=False)
    entropy = Column(Float, nullable=False)
    digit_ratio = Column(Float, nullable=False)
    special_character_ratio = Column(Float, nullable=False)
    unique_character_ratio = Column(Float, nullable=False)
    query_frequency = Column(Float, nullable=False, default=0.0)
    nxdomain_frequency = Column(Float, nullable=False, default=0.0)

    query = relationship("DNSQuery", back_populates="features")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True, nullable=False)
    query_id = Column(Integer, ForeignKey("dns_queries.id", ondelete="CASCADE"), nullable=True, index=True)
    detector = Column(String(50), nullable=False, index=True)
    severity = Column(String(20), nullable=False, index=True)
    risk_score = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    evidence = Column(Text, nullable=False)
    mitre_technique = Column(String(50), nullable=True)
    mitre_name = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False, default="NEW", index=True)

    query = relationship("DNSQuery", back_populates="alerts")
