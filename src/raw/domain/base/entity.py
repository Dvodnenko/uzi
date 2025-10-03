from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .enums import Color, EntityType


@dataclass(eq=False)
class Entity:

    subpath: Path
    type: EntityType
    refs: list[Path]
    color: Color = field(default=Color.WHITE, kw_only=True)
    icon: str | None = field(default=None, kw_only=True)

    @property
    def title(self) -> str:
        return self.subpath.name
    
    def __eq__(self, other):
        return isinstance(other, Entity) and self.subpath == other.subpath

    def getattr(self, atr: str) -> Any:
        keys = atr.split(".")
        result = self.__getattribute__(keys[0])
        for key in keys[1:]:
            result = result.__getattribute__(key)
        return result
