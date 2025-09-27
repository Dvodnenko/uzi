from abc import ABC, abstractmethod
from pathlib import Path

from ..base.entity import Entity


class FileRepository(ABC):

    ext: str = None
    
    @abstractmethod
    def save(self, entity: Entity) -> None: ...

    @abstractmethod
    def load(self, path: Path) -> Entity: ...
