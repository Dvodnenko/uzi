from dataclasses import dataclass, field

from .enums import Color


@dataclass(eq=False)
class Entity:

    title: str # /a/b/c, not just c
    color: Color = Color.WHITE
    icon: str = ""
    description: str = ""

    links: list["Entity"] = field(
        default_factory=lambda: [])
    parent_id: int = None
    parent: "Folder" = None

    def __post_init__(self):
        if not self.title.startswith("/"):
            self.title = f"/{self.title}"

    def __str__(self):
        return self.title

    def update(self, **kwargs):
        new = self
        for key, value in kwargs.items():
            new.__setattr__(key, value)
        new.__post_init__()
        return new

    @property
    def parentstr(self) -> str:
        return self.title[0:self.title.rfind("/")]

    @property
    def name(self) -> str:
        return self.title[self.title.rfind("/")+1 :]
