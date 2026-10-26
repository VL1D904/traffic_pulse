from tracking_pipeline import TrackingPipeline
from video_resolver_factory import VideoResolverFactory
import cv2


class VideoWorker:
    def __init__(self) -> None:
        self.tracking_pipeline = TrackingPipeline()

    def start(self, url: str) -> None:
        video_resolver = VideoResolverFactory.create(url)
        for frame, frame_count in video_resolver.get_frames():
            detected_plot, _ = self.tracking_pipeline.tracking(frame)
            cv2.imshow("video", detected_plot)

            if 0xFF == ord('q') & cv2.waitKey(1):
                break

        cv2.destroyAllWindows()


