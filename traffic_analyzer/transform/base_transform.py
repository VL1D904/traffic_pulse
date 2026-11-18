from abc import ABC, abstractmethod


class BaseTransform(ABC):
    @abstractmethod
    def transform(self, data: dict):
        pass