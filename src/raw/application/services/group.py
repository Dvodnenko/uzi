from ...domain import Group, FileRepository, Config, UseCaseResponse


class GroupService:
    def __init__(self, repo: FileRepository, config: Config):
        self.repo = repo
        self.config = config

    def create(self, group: Group) -> UseCaseResponse[Group]:
        _path = self.config.core.raw_path / group.subpath / f"{group.title}"
        self.repo.load(_path)
        if _path.exists():
            return UseCaseResponse(
                status_code=3,
                message=f"Group already exists: {group.subpath}/{group.title}", 
            )
        _path.mkdir(parents=True)
        self.repo.save(group)
        return UseCaseResponse(
            message=f"Group created: {group.subpath}/{group.title}"
        )
    
    def update(self, subpath: str, new: Group) -> UseCaseResponse[Group]:
        _path = self.config.core.raw_path / subpath
        if not _path.exists() or not _path.is_dir():
            return UseCaseResponse(
                message=f"Group not found: {subpath}", status_code=4
            )
        self.repo.save(new)
        return UseCaseResponse(
            message=f"Group updated: {subpath}"
        )
    
    def delete(self, subpath: str) -> UseCaseResponse[Group]:
        _path = self.config.core.raw_path / subpath
        if not _path.exists() or not _path.is_dir():
            return UseCaseResponse(
                message=f"Group not found: {subpath}", status_code=4
            )
        _path.rmdir()
        return UseCaseResponse(
            message=f"Group deleted: {subpath}"
        )
