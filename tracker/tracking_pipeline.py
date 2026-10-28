from yolo_tracker import YoloTracker
from detection_contract import DetectionContract
from frame_result_contract import FrameResultContract
from typing import List
import time
import numpy as np


class TrackingPipeline:
    def __init__(self):
        self.TRACKER_TTL = 60 * 60
        self.yolo_tracker = YoloTracker()
        self.start_time = time.time()

    def tracking(self, frame: np.ndarray, frame_count: int) -> FrameResultContract:
        current_time = time.time() 
        if (current_time - self.start_time) >= self.TRACKER_TTL:
            self.start_time = current_time
            self.yolo_tracker.reset_tracker()

        detected_plot, detections = self.yolo_tracker.detect_object(frame)
        detection_contracts = self.process_frame(detections, current_time)
        frame_result = FrameResultContract(
            session_id=self.yolo_tracker.get_session_uuid(),
            frame_count=frame_count,
            detections=detection_contracts,
            processed_frame=detected_plot
        )
        return frame_result

    def process_frame(self, detections: np.ndarray, current_time: float) -> List[DetectionContract]:
        detection_contracts = []

        for box in detections:
            if box.id is None:
                continue

            track_id = int(box.id.item())
            track_type_id = int(box.cls.item())
            bbox = box.xyxy.tolist()[0]
            confidence = box.conf.item()
            detection_time = current_time

            detection_contracts.append(
                DetectionContract(
                    track_id=track_id,
                    track_type_id=track_type_id,
                    detection_time=detection_time,
                    bbox=bbox,
                    confidence=confidence
                )
            )

        return detection_contracts

