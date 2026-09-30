from typing import Dict, Any, Optional
from app.detection.base import BaseDetector

class NXDOMAINDetector(BaseDetector):
    def __init__(self): super().__init__("nxdomain")
    def detect(self, query: Dict[str, Any], features: Dict[str, Any], history: Optional[list] = None) -> Dict[str, Any]:
        rcode = query.get("response_code", "NOERROR")
        evidence, confidence = [], 0.0
        if rcode == "NXDOMAIN":
            evidence.append("Query returned NXDOMAIN response")
            confidence += 0.6
        return {
            "detected": confidence >= 0.60, "confidence": confidence, "evidence": evidence,
            "title": "NXDOMAIN Spike / Reconnaissance",
            "description": "Non-existent domain resolution detected.",
            "mitre_technique": "T1568", "mitre_name": "Dynamic Resolution"
        }
