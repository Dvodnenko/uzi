from ..repositories.tag import saTagRepository
from ..repositories.folder import saFolderRepository
from ..entities import Tag
from ..database.funcs import get_all_by_titles
from .decorators import provide_conf, cast_kwargs


class TagService:
    def __init__(self, repository: saTagRepository):
        self.repository = repository
        self.folders_repository = saFolderRepository(repository.session)

    @cast_kwargs(Tag)
    def create(self, args: list, flags: list, **kwargs):
        tag = Tag(**kwargs)
        if next(self.repository.get(tag.title)):
            yield f"Tag already exists: {tag.title}", 1
            return
        next(self.repository.create(tag))
        yield f"Tag created: {tag.title}", 0
    
    @provide_conf
    def all(self, args: list, flags: list, **kwargs):
        sortby = kwargs.get("sortby", "title")
        if "t" in flags:
            for tag in self.repository.get_all(sortby):
                yield tag.title, 0
        else:
            pattern: str = kwargs["__cnf"]["formats"]["tag"]
            for tag in self.repository.get_all(sortby):
                yield pattern.format(**tag.to_dict()), 0
    
    @provide_conf
    def print(self, args: list, flags: list, **kwargs):
        pattern: str = kwargs["__cnf"]["formats"]["tag"]
        for tag in get_all_by_titles(self.repository.session, Tag, args):
            yield pattern.format(**tag.to_dict()), 0
    
    @cast_kwargs(Tag)
    def update(self, args: list, flags: list, **kwargs):
        current = next(self.repository.get(args[0]))
        if not current:
            yield f"Tag not found: {args[0]}", 1
            return
        next(self.repository.update(args[0], **kwargs))
        yield f"Tag updated: {args[0]}", 0

    def delete(self, args: list, flags: list, **kwargs):
        tag = next(self.repository.get(args[0]))
        if not tag:
            yield f"Tag not found: {args[0]}", 1
            return
        next(self.repository.delete(tag))
        yield f"Tag deleted: {args[0]}", 0
