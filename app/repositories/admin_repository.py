from dotenv import load_dotenv
from repositories.base_repository import BaseRepository 
import os
import psycopg2
import bcrypt


load_dotenv()


class AdminRepository(BaseRepository):
    async def add_admin(self, login: str, password: str) -> None:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))

        async with self.pool.acquire() as connection:
            async with connection.transaction():
                query = "insert into admin.admins (login, pwd) values ($1, $2) on conflict do nothing"
                await connection.execute(query, login, hashed_password.decode('utf-8'))

    async def get_password(self, login: str) -> (tuple | None):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                query = "select pwd from admin.admins where login = $1"
                data = await connection.fetchrow(query, login)
                return tuple(data) if data is not None else None

    async def check_admin(self, login: str, password: str) -> bool:
        admin_pwd = await self.get_password(login)
        if not admin_pwd:
            return False
        
        return bcrypt.checkpw(password.encode('utf-8'), admin_pwd[0].encode('utf-8'))