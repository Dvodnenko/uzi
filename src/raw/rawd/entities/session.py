from dataclasses import dataclass, field
from datetime import datetime, timedelta

from .entity import Entity


@dataclass(kw_only=True, eq=False)
class Session(Entity):
    start: datetime
    summary: str = ""
    end: datetime | None = field(default=None, kw_only=True)

    def to_dict(self):
        return {
            ## From Entity
            "title": self.title,
            "color": self.color,
            "icon": self.icon,
            "description": self.description,
            "links": self.links,
            "parent": self.parent,
            "parent_id": self.parent_id,

            ## Sessions's Itself
            "start": self.start,
            "summary": self.summary,
            "end": self.end,

            ## Properties
            "is_active": self.is_active,
            "total": self.total,

            ## Start & End Time
            "sw": self.start.strftime("%a"), # Saturday
            "sd": self.start.strftime("%d"), # 1
            "sm": self.start.strftime("%b"), # February
            "sy": self.start.strftime("%Y"), # 2025
            "sH": self.start.strftime("%H"), # 18
            "sM": self.start.strftime("%M"), # 38
            "sS": self.start.strftime("%S"), # 00

            "ew": self.end.strftime("%a"), # Friday
            "ed": self.end.strftime("%d"), # 31
            "em": self.end.strftime("%b"), # October
            "ey": self.end.strftime("%Y"), # 2025
            "eH": self.end.strftime("%H"), # 16
            "eM": self.end.strftime("%M"), # 11
            "eS": self.end.strftime("%S"), # 09
        }

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
