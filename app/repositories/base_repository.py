from abc import ABC, abstractmethod
from dotenv import load_dotenv
import psycopg2
import os


load_dotenv()


class BaseRepository(ABC):
    def __init__(self) -> None:
        self.CONNECTION = psycopg2.connect(
            dbname=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT")
        )
        
    def close(self):
        self.CONNECTION.close()