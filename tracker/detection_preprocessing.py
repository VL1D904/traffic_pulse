from contracts.frame_result_contract import FrameResultContract
from typing import List


class DetectionPreprocessing:
    @staticmethod
    def preprocess(video_id: int,  frame_result: FrameResultContract) -> List[dict]:
        detections = []

        height, width = frame_result.processed_frame.shape[:2]


        for detection in frame_result.detections:
            detection_dict = {
                "video_id": video_id,
                "session_id": str(frame_result.session_id),
                "track_id": detection.track_id,
                "track_type_id": detection.track_type_id,
                "detection_time": int(detection.detection_time.timestamp() * 1000),
                "bbox_x1_px": int(detection.bbox[0]),
                "bbox_y1_px": int(detection.bbox[1]),
                "bbox_x2_px": int(detection.bbox[2]),
                "bbox_y2_px": int(detection.bbox[3]),
                "frame_count": frame_result.frame_count,
                "confidence": detection.confidence,
                "frame_size": [width, height]
            }

            detections.append(detection_dict)

        return detections