import re
from typing import Dict, Any, Optional
from app.detection.base import BaseDetector

class DGADetector(BaseDetector):
    def __init__(self): super().__init__("dga")
    def detect(self, query: Dict[str, Any], features: Dict[str, Any], history: Optional[list] = None) -> Dict[str, Any]:
        domain_len, entropy = features.get("domain_length", 0), features.get("entropy", 0.0)
        evidence, confidence = [], 0.0
        if entropy > 3.8 and domain_len > 16:
            evidence.append(f"High domain entropy ({entropy:.2f}) for length {domain_len}")
            confidence += 0.6
        confidence = min(round(confidence, 2), 0.90)
        return {
            "detected": confidence >= 0.55, "confidence": confidence, "evidence": evidence,
            "title": "Domain Generation Algorithm (DGA) Suspected",
            "description": "Domain string exhibits pseudo-random features.",
            "mitre_technique": "T1568.002", "mitre_name": "Dynamic Resolution: DGA"
        }
