from dataclasses import dataclass
from typing import Generic, Optional, TypeVar


T = TypeVar("T")

@dataclass
class UseCaseResponse(Generic[T]):
    message: Optional[str] = None
    status_code: int = 0
    data: Optional[T] = None

    @property
    def success(self) -> bool:
        return self.status_code == 0
