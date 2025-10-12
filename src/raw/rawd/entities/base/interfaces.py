from abc import ABC, abstractmethod

from ..base.entity import Entity


class EntityRepository(ABC):
    
    @abstractmethod
    def create(self, entity: Entity) -> None: ...

    @abstractmethod
    def get(self, title: str) -> Entity | None: ...

    @abstractmethod
    def get_all(self) -> list[Entity]: ...

    @abstractmethod
    def update(self, title: str, entity: Entity) -> None: ...

    @abstractmethod
    def delete(self, entity: Entity) -> None: ...
