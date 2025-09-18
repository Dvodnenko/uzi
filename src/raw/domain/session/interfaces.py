from abc import ABC, abstractmethod
from pathlib import Path

from ..session.entity import Session


class SessionRepository(ABC):

    ext: str = None
    
    @abstractmethod
    def save(self, session: Session) -> None: ...

    @abstractmethod
    def load(self, path: Path) -> Session: ...
