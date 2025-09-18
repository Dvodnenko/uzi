from abc import ABC, abstractmethod
from pathlib import Path

from ..tag.entity import Tag


class TagRepository(ABC):

    ext: str = None
    
    @abstractmethod
    def save(self, tag: Tag) -> None: ...

    @abstractmethod
    def load(self, path: Path) -> Tag: ...
