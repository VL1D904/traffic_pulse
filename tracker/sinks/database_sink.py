from sinks.base_sink import BaseSink
from contracts.frame_result_contract import FrameResultContract
from video_status import VideoStatus
from dotenv import load_dotenv
import os
import asyncpg
from datetime import datetime, timezone


load_dotenv()


class DatabaseSink(BaseSink):
    def __init__(self) -> None:
        self.connection: asyncpg.Connection | None = None

    async def connect(self):
        self.connection = await asyncpg.connect(
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT"),
        )

    async def close(self):
        await self.connection.close()

    async def send(self, frame_result: FrameResultContract, video_id: int):
        pass

    async def set_video_status(self, video_id: int, video_status: VideoStatus) -> None:
        query = "update raw.video_sources set status = $1 where id = $2"
        await self.connection.execute(query, video_status.value, video_id)

    async def start_recording(self, video_id: int) -> None:
        recording_at = datetime.now()
        query = """insert into raw.video_recording (video_source_id, recording_at)
                values ($1, $2)
                returning id
                """
        recording_id = await self.connection.fetchval(query, video_id, recording_at)
        return recording_id

    async def stop_recording(self, recording_id: int) -> None:
        recording_end = datetime.now()
        query = "update raw.video_recording set recording_end = $1 where id = $2"
        await self.connection.execute(query, recording_end, recording_id)