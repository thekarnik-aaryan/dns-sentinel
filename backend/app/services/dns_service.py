import datetime
from sqlalchemy.orm import Session
from app.database import models
from app.features.dns_features import extract_all_features
from app.detection.dns_tunneling import DNSTunnelingDetector
from app.detection.dga import DGADetector
from app.detection.nxdomain import NXDOMAINDetector
from app.scoring.risk_engine import RiskEngine
from app.ml.anomaly_detector import DNSAnomalyDetector

tunnel_detector, dga_detector, nx_detector = DNSTunnelingDetector(), DGADetector(), NXDOMAINDetector()
risk_engine, ml_detector = RiskEngine(), DNSAnomalyDetector()

def process_incoming_query(db: Session, raw_query: dict) -> models.DNSQuery:
    query_obj = models.DNSQuery(
        timestamp=raw_query.get("timestamp", datetime.datetime.utcnow()),
        source_ip=raw_query.get("source_ip", "127.0.0.1"),
        destination_ip=raw_query.get("destination_ip", "8.8.8.8"),
        query_name=raw_query.get("query_name", "example.com"),
        query_type=raw_query.get("query_type", "A"),
        response_code=raw_query.get("response_code", "NOERROR"),
        packet_size=raw_query.get("packet_size", 64),
        response_time=raw_query.get("response_time", 15.0)
    )
    db.add(query_obj)
    db.flush()

    recent_count = db.query(models.DNSQuery).filter(models.DNSQuery.source_ip == query_obj.source_ip).count()
    nx_count = db.query(models.DNSQuery).filter(models.DNSQuery.source_ip == query_obj.source_ip, models.DNSQuery.response_code == "NXDOMAIN").count()

    feats = extract_all_features(query_obj.query_name, float(recent_count), float(nx_count) / max(recent_count, 1))
    db.add(models.DNSFeature(query_id=query_obj.id, **feats))

    r_tunnel = tunnel_detector.detect(raw_query, feats)
    r_tunnel["detector"] = "dns_tunneling"
    r_dga = dga_detector.detect(raw_query, feats)
    r_dga["detector"] = "dga"
    r_nx = nx_detector.detect(raw_query, feats)
    r_nx["detector"] = "nxdomain"

    ml_res = ml_detector.predict(feats)
    eval_result = risk_engine.evaluate([r_tunnel, r_dga, r_nx], ml_res)

    if eval_result["risk_score"] >= 25.0:
        db.add(models.Alert(
            timestamp=query_obj.timestamp, query_id=query_obj.id, detector=eval_result["detector"],
            severity=eval_result["severity"], risk_score=eval_result["risk_score"], confidence=eval_result["confidence"],
            title=eval_result["title"], description=eval_result["description"], evidence=eval_result["evidence"],
            mitre_technique=eval_result["mitre_technique"], mitre_name=eval_result["mitre_name"], status="NEW"
        ))

    db.commit()
    db.refresh(query_obj)
    return query_obj
