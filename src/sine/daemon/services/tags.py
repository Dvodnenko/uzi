from ..repositories.tag import saTagRepository
from ..repositories.folder import saFolderRepository
from ..entities import Tag
from ..database.funcs import get_all_by_titles, filter
from .decorators import cast_kwargs
from .base import Service
from ...common import load_config, parse_afk, drill, CONFIG_GLOBALS
from ...common.constants import DEFAULT_FMT
from ..funcs import asexc


PARSER = parse_afk
class TagService(Service):
    def __init__(self, repository: saTagRepository):
        self.repository = repository
        self.folders_repository = saFolderRepository(repository.session)

    def execute(self, rspd):
        if not hasattr(self, rspd["source"][1]):
            yield f"Command not found: {rspd["source"][1]}", 1
            return
        try:
            gen = getattr(self, rspd["source"][1])(rspd)
            yield from gen
        except Exception as e:
            yield asexc(e), 1

    @cast_kwargs(Tag)
    def create(self, rspd: dict):
        _, _, kwargs = rspd["ps"]["afk"]
        if not kwargs.get("styles") and kwargs.get("parent"):
            kwargs["styles"] = kwargs["parent"].styles
        tag = Tag(**kwargs)
        if next(self.repository.get(tag.title)):
            yield f"Tag already exists: {tag.title}", 1
            return
        next(self.repository.create(tag))
        yield f"Tag created: {tag.title}", 0
    
    def all(self, rspd: dict):
        _, flags, kwargs = rspd["ps"]["afk"]
        sortby = kwargs.pop("sortby", "title")
        if "t" in flags:
            for tag in self.repository.get_all(sortby):
                yield tag.title, 0
        else:
            config = load_config()
            fmt = kwargs.get("fmt", "0")
            pattern: str = drill(
                config, ["output", "tags", "formats", fmt], default=DEFAULT_FMT)
            for tag in self.repository.get_all(sortby):
                yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": tag}), 0

    def filter(self, rspd: dict):
        _, flags, kwargs = rspd["ps"]["afk"]
        filters = rspd["ps"]["sql"]
        sortby = kwargs.pop("sortby", "title")
        fmt = kwargs.pop("fmt", "0")
        if "t" in flags:
            for tag in filter(self.repository.session, Tag, filters, sortby):
                yield tag.title, 0
        else:
            config = load_config()
            pattern: str = drill(
                config, ["output", "tags", "formats", fmt], default=DEFAULT_FMT)
            for tag in filter(self.repository.session, Tag, filters, sortby):
                yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": tag}), 0
    
    def print(self, rspd: dict):
        args, _, kwargs = rspd["ps"]["afk"]
        config = load_config()
        fmt = kwargs.pop("fmt", "0")
        pattern: str = drill(
            config, ["output", "tags", "formats", fmt], default=DEFAULT_FMT)
        for tag in get_all_by_titles(self.repository.session, Tag, args):
            yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": tag}), 0
    
    @cast_kwargs(Tag)
    def update(self, rspd: dict):
        args, _, kwargs = rspd["ps"]["afk"]
        current = next(self.repository.get(args[2]))
        if not current:
            yield f"Tag not found: {args[2]}", 1
            return
        next(self.repository.update(args[2], **kwargs))
        yield f"Tag updated: {args[2]}", 0

    def delete(self, rspd: dict):
        args, _, _ = rspd["ps"]["afk"]
        tag = next(self.repository.get(args[2]))
        if not tag:
            yield f"Tag not found: {args[2]}", 1
            return
        next(self.repository.delete(tag))
        yield f"Tag deleted: {args[2]}", 0
