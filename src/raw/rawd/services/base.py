from abc import ABC, abstractmethod
from typing import Any


class BaseService(ABC):

    @abstractmethod
    def cast_kwargs(self, **kwargs) -> dict[str, Any]:
        ...
