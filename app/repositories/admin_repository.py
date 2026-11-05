from dotenv import load_dotenv
from repositories.base_repository import BaseRepository 
import os
import psycopg2
import bcrypt


load_dotenv()


class AdminRepository(BaseRepository):
    def add_admin(self, login: str, password: str) -> None:
        try:
            with self.CONNECTION.cursor() as cursor:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
                query = "insert into admin.admins (login, pwd) values (%s, %s) on conflict do nothing"
                cursor.execute(query, (login, hashed_password.decode('utf-8')))
                self.CONNECTION.commit()
        except psycopg2.Error as ex:
            self.CONNECTION.rollback()
            raise ex

    def get_password(self, login: str) -> (tuple | None):
        with self.CONNECTION.cursor() as cursor:
            query = "select pwd from admin.admins where login = %s"
            cursor.execute(query, (login,))
            data = cursor.fetchone()
            return data

    def check_admin(self, login: str, password: str) -> bool:
        admin_pwd = self.get_password(login)
        if not admin_pwd:
            return False
        
        return bcrypt.checkpw(password.encode('utf-8'), admin_pwd[0].encode('utf-8'))