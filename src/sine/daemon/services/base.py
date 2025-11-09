from abc import ABC, abstractmethod
from typing import Generator


class Service(ABC):
    
    @abstractmethod
    def execute(self, argv: list[str]) -> Generator:
        ...

    def _get(self, attribute: str, default=None):
        try:
            return getattr(self, attribute)
        except AttributeError:
            return default
