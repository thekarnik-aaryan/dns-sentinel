import os, joblib, numpy as np
from typing import Dict, Any, Optional

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../../ml/models/isolation_forest.joblib")

class DNSAnomalyDetector:
    def __init__(self):
        self.model = None
        if os.path.exists(MODEL_PATH):
            try: self.model = joblib.load(MODEL_PATH)
            except Exception: pass

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        if self.model is None: return {"detected": False, "score": 0.0, "confidence": 0.0}
        vector = np.array([[
            features.get("domain_length", 0), features.get("subdomain_length", 0),
            features.get("entropy", 0.0), features.get("digit_ratio", 0.0),
            features.get("unique_character_ratio", 0.0), features.get("query_frequency", 0.0),
            features.get("nxdomain_frequency", 0.0)
        ]])
        pred = self.model.predict(vector)[0]
        score = -float(self.model.score_samples(vector)[0])
        detected = bool(pred == -1)
        return {"detected": detected, "score": round(score, 4), "confidence": min(round(score * 1.2, 2), 0.95) if detected else 0.0}
