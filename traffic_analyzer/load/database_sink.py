from dotenv import load_dotenv
from typing import Optional
import asyncpg
import os


load_dotenv()


class DatabaseSink:
    def __init__(self):
        def __init__(self) -> None:
                self.connection: Optional[asyncpg.Connection] = None
        
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