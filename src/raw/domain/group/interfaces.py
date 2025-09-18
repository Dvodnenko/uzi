from abc import ABC, abstractmethod
from pathlib import Path

from .entity import Group


class GroupRepository(ABC):

    ext: str = None
    
    @abstractmethod
    def save(self, group: Group) -> None: ...

    @abstractmethod
    def load(self, path: Path) -> Group: ...
