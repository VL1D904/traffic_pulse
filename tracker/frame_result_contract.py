from pydantic import BaseModel, ConfigDict, UUID4
from typing import List
from detection_contract import DetectionContract
import numpy as np


class FrameResultContract(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    session_id: UUID4
    frame_count: int
    detections: List[DetectionContract]
    processed_frame: np.ndarray