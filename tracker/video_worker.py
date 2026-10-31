from tracking_pipeline import TrackingPipeline
from video_resolver_factory import VideoResolverFactory
from websocket_sink import WebSocketSink
import asyncio
import multiprocessing


class VideoWorker:
    def __init__(self, video_id: int, stop_event: multiprocessing.Event) -> None:
        self.video_id = video_id
        self.stop_event = stop_event
        self.tracking_pipeline = TrackingPipeline()
        self.websocket_sink = WebSocketSink()

    async def start(self, url: str) -> None:
        await self.websocket_sink.connect()

        try:
            video_resolver = VideoResolverFactory.create(url)
            for frame, frame_count in video_resolver.get_frames():
                if self.stop_event.is_set():
                    break

                frame_result = await asyncio.to_thread(
                    self.tracking_pipeline.tracking, frame, frame_count
                )

                if self.stop_event.is_set():
                    break

                await self.websocket_sink.send_plot(frame_result, self.video_id)
        except asyncio.CancelledError:
            raise
        except Exception as ex:
            print(f'Воркер {self.video_id} Ошибка {ex}')
        finally:
            try:
                print(f"[Worker {self.video_id}] Graceful shutdown: закрываем WebSocket")
                await asyncio.shield(self.websocket_sink.close())
            except asyncio.CancelledError:
                print(f"[Worker {self.video_id}] Принудительное закрытие WebSocket")
                try:
                    if hasattr(self.websocket_sink, 'websocket') and self.websocket_sink.websocket:
                        await self.websocket_sink.websocket.close()
                except Exception:
                    pass
            except Exception as e:
                print(f"[Worker {self.video_id}] Ошибка при закрытии WebSocket: {e}")
            
            


