from abc import ABC, abstractmethod
from contracts.frame_result_contract import FrameResultContract


# Абстрактный класс для передачи данных между сервисами
class BaseSink:
    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    @abstractmethod
    async def send(self, frame_result: FrameResultContract, video_id: int) -> None:
        pass