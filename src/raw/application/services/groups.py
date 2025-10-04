from pathlib import Path

from ...domain import Group, EntityRepository, Config, UseCaseResponse


class GroupService:
    def __init__(
            self, 
            repository: EntityRepository, 
            config: Config
    ):
        self.repository = repository
        self.config = config

    def create(self, group: Group) -> None:
        if self.repository.get(group.title):
            return UseCaseResponse(f"Group already exists: {group.title}", status_code=5)
        if not self.repository.get(group.title.parent):
            return UseCaseResponse(f"Group not found: {group.title.parent}", status_code=4)
        self.repository.create(group)
        return UseCaseResponse(f"Group created: {group.title}")
        
    def update(self, title: Path, new: Group):
        if not self.repository.get(title):
            return UseCaseResponse(f"Group not found: {title}", status_code=4)
        if self.repository.get(new.title):
            return UseCaseResponse(f"Group already exists: {new.title}", status_code=5)
        self.repository.update(title, new)
        return UseCaseResponse(f"Group updated: {title}")
