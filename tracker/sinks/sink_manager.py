from sinks.base_sink import BaseSink
from typing import List, Coroutine
from contracts.frame_result_contract import FrameResultContract
import asyncio


class SinkManager:
    def __init__(self, sinks: List[BaseSink]) -> None:
        self.sinks = sinks

    async def complete_tasks(self, tasks: List[Coroutine]) -> None:
        if not tasks:
            return
        
        try:
            await asyncio.wait_for(asyncio.gather(*tasks), timeout=10.0)
        except asyncio.TimeoutError:
            print("Превышено время ожидания выполнения задачи")
            raise

    async def connect_all(self) -> None:
        tasks = [sink.connect() for sink in self.sinks]
        await self.complete_tasks(tasks)

    async def close_all(self) -> None:
        tasks = [sink.close() for sink in self.sinks]
        await self.complete_tasks(tasks)

    async def send_all(self, frame_result: FrameResultContract, video_id: int) -> None:
        tasks = [sink.send(frame_result, video_id) for sink in self.sinks]
        await self.complete_tasks(tasks)

