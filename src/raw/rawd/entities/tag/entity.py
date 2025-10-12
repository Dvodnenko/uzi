from dataclasses import dataclass

from ...domain.base.entity import Entity


@dataclass(kw_only=True, eq=False)
class Tag(Entity):
    ...
