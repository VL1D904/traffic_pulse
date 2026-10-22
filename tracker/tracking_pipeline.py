from yolo_tracker import YoloTracker
import time


class TrackingPipeline:
    def __init__(self):
        self.TRACKER_TTL = 60 * 60
        self.yolo_tracker = YoloTracker()
        self.start_time = time.time()

    def tracking(self, frame):
        current_time = time.time() 
        if (current_time - self.start_time) >= self.TRACKER_TTL:
            self.start_time = current_time
            self.yolo_tracker.reset_tracker()

        self.yolo_tracker.detect_object(frame)

