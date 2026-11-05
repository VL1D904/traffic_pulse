from processing_pipeline import ProcessingPipeline
from sinks.websocket_sink import WebSocketSink
from sinks.database_sink import DatabaseSink
from sinks.sink_manager import SinkManager
from video_status import VideoStatus
import signal
import asyncio
import multiprocessing

class VideoWorker:
    def __init__(self, video_id: int, stop_event: multiprocessing.Event) -> None:
        self.video_id = video_id
        self.stop_event = stop_event
        self.recording_id: int | None = None
        
        self.websocket_sink = WebSocketSink()
        self.database_sink = DatabaseSink()
        self.sink_manager = SinkManager([self.websocket_sink, self.database_sink])

        self.processing_pipeline = ProcessingPipeline(
            self.sink_manager
        )

    async def event_listening(self):
        await asyncio.to_thread(self.stop_event.wait)

    async def start(self, url: str) -> None:
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGTERM, lambda: self.stop_event.set())
        having_error = False

        try:
            await self.sink_manager.connect_all()
            self.recording_id = await self.database_sink.start_recording(self.video_id)
            await self.database_sink.set_video_status(self.video_id, VideoStatus.CANCELED)

            task_processing = asyncio.create_task(self.processing_pipeline.run(url, self.video_id))
            task_event_listening = asyncio.create_task(self.event_listening())  
            await self.database_sink.set_video_status(self.video_id, VideoStatus.ACTIVE)

            done, pending = await asyncio.wait({task_event_listening, task_processing}, return_when='FIRST_COMPLETED')

            await self.database_sink.set_video_status(self.video_id, VideoStatus.CANCELED)

            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

            for task in done:
                task.result()

        except Exception as ex:
            having_error = True
            await self.database_sink.set_video_status(self.video_id, VideoStatus.ERROR)
            print(f"Произошла ошибка worker:{self.video_id}: {ex}")
        finally:
            if not having_error:
                await self.database_sink.set_video_status(self.video_id, VideoStatus.INACTIVE)
            if self.recording_id is not None:
                await self.database_sink.stop_recording(self.recording_id)
            await self.sink_manager.close_all()
            


