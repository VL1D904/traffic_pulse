from abc import ABC 
import asyncpg


class BaseRepository(ABC):
    def __init__(self, pool: asyncpg.Pool) -> None:
        self.pool: asyncpg.Pool = pool
        
    async def close(self):
        await self.pool.close()