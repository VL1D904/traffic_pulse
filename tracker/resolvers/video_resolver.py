from abc import ABC, abstractmethod
from typing import Generator


# Абстрактный класс для чтения кадров из видеопотока
class VideoResolver(ABC):
    def __init__(self, video_url: str) -> None:
        self.video_url = video_url

    # Абстрактный метод получения кадров из видеопотока
    @abstractmethod
    def get_frames(self) -> Generator:
        pass