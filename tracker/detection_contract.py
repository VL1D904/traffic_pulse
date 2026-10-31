from pydantic import BaseModel
from datetime import datetime
from typing import List


# Контракт для детекций
class DetectionContract(BaseModel):
    track_id: int
    track_type_id: int
    detection_time: datetime
    bbox: List[float]
    confidence: float