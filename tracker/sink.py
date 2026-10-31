from abc import ABC, abstractmethod


# Абстрактный класс для передачи данных между сервисами
class Sink:
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass