from tracking_pipeline import TrackingPipeline
from video_resolver_factory import VideoResolverFactory
from websocket_sink import WebSocketSink
import asyncio


class VideoWorker:
    def __init__(self, video_id: int) -> None:
        self.video_id = video_id
        self.tracking_pipeline = TrackingPipeline()
        self.websocket_sink = WebSocketSink()

    async def start(self, url: str) -> None:
        await self.websocket_sink.connect()

        video_resolver = VideoResolverFactory.create(url)
        for frame, frame_count in video_resolver.get_frames():
            frame_result = await asyncio.to_thread(
                self.tracking_pipeline.tracking, frame, frame_count
            )

            await self.websocket_sink.send_plot(frame_result, self.video_id)

        await self.websocket_sink.close()
            
            


