from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseDetector(ABC):
    def __init__(self, name: str): self.name = name
    @abstractmethod
    def detect(self, query: Dict[str, Any], features: Dict[str, Any], history: Optional[list] = None) -> Dict[str, Any]: pass
