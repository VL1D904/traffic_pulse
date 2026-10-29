from abc import ABC, abstractmethod


class Sink:
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass