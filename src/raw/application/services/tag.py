from ...domain import Tag, EntityRepository, Config, UseCaseResponse


class TagService:
    def __init__(self, repo: EntityRepository, config: Config):
        self.repo = repo
        self.config = config
        self.ending = "-TAG"
    
    def create(self, tag: Tag) -> UseCaseResponse[Tag]:
        _path = self.config.core.rootgroup / tag.subpath / f"{tag.title}{self.ending}"
        if _path.exists():
            return UseCaseResponse(
                status_code=3,
                message=f"Tag already exists: {tag.subpath}/{tag.title}", 
            )
        _path.touch()
        self.repo.dump(tag)
        return UseCaseResponse(
            message=f"Tag created: {tag.subpath}/{tag.title}"
        )
    
    def delete(self, subpath: str) -> UseCaseResponse[Tag]:
        _path = self.config.core.rootgroup / f"{subpath}{self.ending}"
        if not _path.exists() or not _path.is_file():
            return UseCaseResponse(
                message=f"Tag not found: {subpath}", status_code=4
            )
        _path.unlink()
        return UseCaseResponse(
            message=f"Tag deleted: {subpath}"
        )
