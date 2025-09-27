from dataclasses import dataclass

from src.raw.domain.base.entity import Entity


@dataclass(kw_only=True, eq=False)
class Tag(Entity):
    ...
