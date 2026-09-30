import math
from typing import Dict, Any

def calculate_entropy(text: str) -> float:
    if not text: return 0.0
    prob = [float(text.count(c)) / len(text) for c in set(text)]
    return -sum(p * math.log2(p) for p in prob)

def calculate_digit_ratio(text: str) -> float:
    if not text: return 0.0
    return float(sum(c.isdigit() for c in text)) / len(text)

def calculate_special_char_ratio(text: str) -> float:
    if not text: return 0.0
    return float(sum(not c.isalnum() and c != '.' for c in text)) / len(text)

def calculate_unique_char_ratio(text: str) -> float:
    if not text: return 0.0
    return float(len(set(text))) / len(text)

def extract_subdomain(domain: str) -> str:
    domain = domain.rstrip('.')
    parts = domain.split('.')
    if len(parts) <= 2: return ""
    return ".".join(parts[:-2])

def extract_all_features(query_name: str, query_frequency: float = 0.0, nxdomain_frequency: float = 0.0) -> Dict[str, Any]:
    clean_name = query_name.strip().rstrip('.')
    subdomain = extract_subdomain(clean_name)
    return {
        "domain_length": len(clean_name),
        "subdomain_length": len(subdomain),
        "entropy": round(calculate_entropy(clean_name), 4),
        "digit_ratio": round(calculate_digit_ratio(clean_name), 4),
        "special_character_ratio": round(calculate_special_char_ratio(clean_name), 4),
        "unique_character_ratio": round(calculate_unique_char_ratio(clean_name), 4),
        "query_frequency": round(query_frequency, 2),
        "nxdomain_frequency": round(nxdomain_frequency, 4)
    }
