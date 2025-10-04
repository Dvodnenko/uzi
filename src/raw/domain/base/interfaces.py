from abc import ABC, abstractmethod
from pathlib import Path

from ..base.entity import Entity


class EntityRepository(ABC):
    
    @abstractmethod
    def create(self, entity: Entity) -> None: ...

    @abstractmethod
    def get(self, title: Path) -> Entity | None: ...

    @abstractmethod
    def get_all(self) -> list[Entity]: ...

    @abstractmethod
    def update(self, title: Path, entity: Entity) -> None: ...

    @abstractmethod
    def delete(self, title: Path) -> None: ...
