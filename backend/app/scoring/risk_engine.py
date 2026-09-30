import json
from typing import Dict, Any, List, Optional

class RiskEngine:
    WEIGHTS = {"dns_tunneling": 35.0, "dga": 25.0, "beaconing": 25.0, "nxdomain": 20.0, "volume": 15.0, "ml_anomaly": 15.0}

    def evaluate(self, detection_results: List[Dict[str, Any]], ml_result: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        raw_score, all_evidence, highest_conf, highest_detector = 0.0, [], 0.0, "rule_engine"
        title, description, mitre_tech, mitre_name = "Suspicious DNS Behavior", "Indicators triggered", "T1071.004", "DNS"

        for res in detection_results:
            if res.get("detected"):
                det_name = res.get("detector", "rule")
                conf = res.get("confidence", 0.5)
                raw_score += self.WEIGHTS.get(det_name, 15.0) * conf
                all_evidence.extend(res.get("evidence", []))
                if conf > highest_conf:
                    highest_conf, highest_detector = conf, det_name
                    title, description = res.get("title", title), res.get("description", description)
                    mitre_tech, mitre_name = res.get("mitre_technique", mitre_tech), res.get("mitre_name", mitre_name)

        normalized_score = min(round(raw_score, 1), 100.0)
        severity = "CRITICAL" if normalized_score >= 80 else ("HIGH" if normalized_score >= 60 else ("MEDIUM" if normalized_score >= 30 else "LOW"))

        return {
            "risk_score": normalized_score, "severity": severity, "confidence": round(highest_conf, 2),
            "detector": highest_detector, "title": title, "description": description,
            "evidence": json.dumps(all_evidence), "mitre_technique": mitre_tech, "mitre_name": mitre_name
        }
