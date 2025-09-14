import uuid
from dataclasses import dataclass, field


@dataclass(eq=False)
class Entity:

    ID: str = field(init=False, 
                    default=uuid.uuid4().hex)
    group: str # path to the parent folder
    
    @property
    def short_ID(self): 
        return self.ID[:10]
