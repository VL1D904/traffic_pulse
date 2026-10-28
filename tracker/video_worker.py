from tracking_pipeline import TrackingPipeline
from video_resolver_factory import VideoResolverFactory
import cv2


class VideoWorker:
    def __init__(self) -> None:
        self.tracking_pipeline = TrackingPipeline()

    def start(self, url: str) -> None:
        video_resolver = VideoResolverFactory.create(url)
        for frame, frame_count in video_resolver.get_frames():
            frame_result = self.tracking_pipeline.tracking(frame, frame_count)
            print(frame_result)
            


