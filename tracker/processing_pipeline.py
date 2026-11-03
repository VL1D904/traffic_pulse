from resolvers.video_resolver_factory import VideoResolverFactory
from tracking_pipeline import TrackingPipeline
from sinks.sink_manager import SinkManager
import asyncio


class ProcessingPipeline:
    def __init__(
            self,
            sink_manager: SinkManager,
    ) -> None:
        self.sink_manager = sink_manager
        self.tracking_pipeline = TrackingPipeline()

    async def run(self, url: str, video_id: int) -> None:
        video_resolver = VideoResolverFactory.create(url)
        for frame, frame_count in video_resolver.get_frames():
            frame_result = await asyncio.to_thread(
                self.tracking_pipeline.tracking, frame, frame_count
            )

            await self.sink_manager.send_all(frame_result, video_id)
