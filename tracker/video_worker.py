from video_resolver_factory import VideoResolverFactory
from yolo_tracker import YoloTracker
import cv2


video_resolver = VideoResolverFactory.create("https://vkvideo.ru/video-143491903_456240262?t=497970544h40m32s")
tracker = YoloTracker()
for frame, _ in video_resolver.get_frames():
    tracker.detect_object(frame)

    cv2.imshow("vk", tracker.get_detected_plot())

    if 0xFF == ord('q') & cv2.waitKey(1):
        break


cv2.destroyAllWindows()

