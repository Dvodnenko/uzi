from dataclasses import dataclass, field
from pathlib import Path

from .enums import Color, EntityType


@dataclass(eq=False)
class Entity:

    subpath: Path
    title: str
    type: EntityType
    color: Color = field(default=Color.WHITE, kw_only=True)
    icon: str | None = field(default=None, kw_only=True)
    
    def __eq__(self, other):
        return isinstance(other, Entity) and self.subpath == other.subpath
