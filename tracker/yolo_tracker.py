from ultralytics import YOLO
import uuid


class YoloTracker:
    def __init__(self, yolo_model_name: str = "yolo26m.pt"):
        self.OBJECT_CLASSES = [0, 1, 2, 3, 5, 7]

        self.yolo_model_name = yolo_model_name
        self.yolo_model = YOLO(self.yolo_model_name)
        self.session_uuid = uuid.uuid4()

    def get_session_uuid(self):
        return self.session_uuid

    def reset_tracker(self) -> tuple:
        self.yolo_model = YOLO(self.yolo_model_name)
        self.session_uuid = uuid.uuid4()

    def detect_object(self, frame) -> None:
        result = self.yolo_model.track(frame,
                                       persist=True,
                                       tracker='bytetrack.yaml',
                                       classes=self.OBJECT_CLASSES,
                                       imgsz=1088,
                                       conf=0.35,
                                       verbose=False)

        detected_plot = result[0].plot(
            line_width=2,
            font_size=.4,
            probs=False
        )

        detections = result[0].boxes
        return (detected_plot, detections)