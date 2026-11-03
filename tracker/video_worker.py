from tracking_pipeline import TrackingPipeline
from processing_pipeline import ProcessingPipeline
from sinks.websocket_sink import WebSocketSink
from sinks.sink_manager import SinkManager
import signal
import asyncio
import multiprocessing

class VideoWorker:
    def __init__(self, video_id: int, stop_event: multiprocessing.Event) -> None:
        self.video_id = video_id
        self.stop_event = stop_event
        
        self.websocket_sink = WebSocketSink()
        self.sink_manager = SinkManager([self.websocket_sink])

        self.processing_pipeline = ProcessingPipeline(
            self.sink_manager
        )

    async def event_listening(self):
        await asyncio.to_thread(self.stop_event.wait)

    async def start(self, url: str) -> None:
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGTERM, lambda: self.stop_event.set())

        try:
            await self.sink_manager.connect_all()

            task_processing = asyncio.create_task(self.processing_pipeline.run(url, self.video_id))
            task_event_listening = asyncio.create_task(self.event_listening())

            done, pending = await asyncio.wait({task_event_listening, task_processing}, return_when='FIRST_COMPLETED')

            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

        except Exception as ex:
            print(f"Произошла ошибка worker:{self.video_id}: {ex}")
        finally:
            await self.sink_manager.close_all()
            


