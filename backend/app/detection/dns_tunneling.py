from typing import Dict, Any, Optional
from app.detection.base import BaseDetector

class DNSTunnelingDetector(BaseDetector):
    def __init__(self): super().__init__("dns_tunneling")
    def detect(self, query: Dict[str, Any], features: Dict[str, Any], history: Optional[list] = None) -> Dict[str, Any]:
        sub_len = features.get("subdomain_length", 0)
        entropy = features.get("entropy", 0.0)
        evidence, confidence = [], 0.0
        if sub_len > 35:
            evidence.append(f"Excessive subdomain length ({sub_len} chars)")
            confidence += 0.5
        if entropy > 4.2:
            evidence.append(f"High Shannon entropy in domain ({entropy:.2f})")
            confidence += 0.4
        confidence = min(round(confidence, 2), 0.95)
        return {
            "detected": confidence >= 0.50, "confidence": confidence, "evidence": evidence,
            "title": "Possible DNS Tunneling / Data Exfiltration",
            "description": "Subdomain characteristics match tunneling software patterns.",
            "mitre_technique": "T1071.004", "mitre_name": "Application Layer Protocol: DNS"
        }
