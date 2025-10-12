from dataclasses import dataclass, field
from typing import Optional

from .enums import Color


@dataclass(eq=False)
class Entity:

    title: str # "a/b/c", not just "c"
    refs: list["Entity"]
    parent_id: Optional[int] = None
    parent: Optional["Entity"] = None
    children: list["Entity"] = None
    color: Color = field(default=Color.WHITE, kw_only=True)
    icon: str | None = field(default=None, kw_only=True)

    def __post_init__(self):
        if not self.title.startswith("/"):
            self.title = f"/{self.title}"

    @property
    def parentstr(self) -> str:
        return self.title[0:self.title.rfind("/")]

    @property
    def name(self) -> str:
        return self.title[self.title.rfind("/")+1 :]
