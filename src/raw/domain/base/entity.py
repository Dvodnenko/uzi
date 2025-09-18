from dataclasses import dataclass
from pathlib import Path


@dataclass(eq=False)
class Entity:

    ID: int
    group: Path # path to the parent folder
    title: str
    
    @property
    def short_ID(self): 
        return self.ID[:10]
    
    def __eq__(self, other):
        return isinstance(other, Entity) and self.ID == other.ID
