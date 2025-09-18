from dataclasses import dataclass

from ..base.entity import Entity


@dataclass(kw_only=True)
class Group(Entity):
    ...
