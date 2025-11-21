from dataclasses import dataclass, field
from datetime import datetime, timedelta

from .entity import Entity


@dataclass(kw_only=True, eq=False)
class Session(Entity):
    start: datetime
    summary: str = ""
    end: datetime = field(default=None, kw_only=True)

    @property
    def is_active(self) -> bool:
        "Wether the Session is active"
        return self.end is None

    @property
    def total(self) -> timedelta:
        if self.is_active:
            return datetime.now().replace(microsecond=0) - self.start
        res = self.end - self.start
        return res
