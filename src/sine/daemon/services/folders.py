from ..repositories.folder import saFolderRepository
from ..entities import Folder
from ..database.funcs import get_all_by_titles, filter
from .decorators import cast_kwargs
from .base import Service
from ...common import load_config, drill, CONFIG_GLOBALS
from ...common.constants import DEFAULT_FMT
from ..funcs import asexc


class FolderService(Service):

    def __init__(self, repository: saFolderRepository):
        self.repository = repository

    def execute(self, rspd):
        if not hasattr(self, rspd["source"][1]):
            yield f"Command not found: {rspd["source"][1]}", 1
            return
        try:
            gen = getattr(self, rspd["source"][1])(rspd)
            yield from gen
        except Exception as e:
            yield asexc(e), 1

    @cast_kwargs(Folder)
    def create(self, rspd: dict):
        _, _, kwargs = rspd["ps"]["afk"]
        if not kwargs.get("styles") and kwargs.get("parent"):
            kwargs["styles"] = kwargs["parent"].styles
        folder = Folder(**kwargs)
        if next(self.repository.get(folder.title)):
            yield f"Folder already exists: {folder.title}", 1
            return
        next(self.repository.create(folder))
        yield f"Folder created: {folder.title}", 0
    
    def all(self, rspd: dict):
        _, flags, kwargs = rspd["ps"]["afk"]
        sortby = kwargs.pop("sortby", "title")
        if "t" in flags:
            for folder in self.repository.get_all(sortby):
                yield folder.title, 0
        else:
            config = load_config()
            fmt = kwargs.get("fmt", "0")
            pattern: str = drill(
                config, ["output", "folders", "formats", fmt], default=DEFAULT_FMT)
            for folder in self.repository.get_all(sortby):
                yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": folder}), 0

    def filter(self, rspd: dict):
        _, flags, kwargs = rspd["ps"]["afk"]
        filters = rspd["ps"]["sql"]
        print("filters", filters, flush=True)
        sortby = kwargs.pop("sortby", "title")
        fmt = kwargs.pop("fmt", "0")
        if "t" in flags:
            for folder in filter(self.repository.session, Folder, filters, sortby):
                yield folder.title, 0
        else:
            config = load_config()
            pattern: str = drill(
                config, ["output", "folders", "formats", fmt], default=DEFAULT_FMT)
            for folder in filter(self.repository.session, Folder, filters, sortby):
                yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": folder}), 0
    
    def print(self, rspd: dict):
        args, _, kwargs = rspd["ps"]["afk"]
        config = load_config()
        fmt = kwargs.pop("fmt", "0")
        pattern: str = drill(
            config, ["output", "folders", "formats", fmt], default=DEFAULT_FMT)
        for folder in get_all_by_titles(self.repository.session, Folder, args):
            yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": folder}), 0

    @cast_kwargs(Folder)
    def update(self, rspd: dict):
        args, _, kwargs = rspd["ps"]["afk"]
        current = next(self.repository.get(args[2]))
        if not current:
            yield f"Folder not found: {args[2]}", 1
        next(self.repository.update(args[2], **kwargs))
        yield f"Folder updated: {args[2]}", 0

    def delete(self, rspd: dict):
        args, flags, _ = rspd["ps"]["afk"]
        folder = next(self.repository.get(args[2]))
        delete = False
        if not folder:
            yield f"Folder not found: {args[2]}", 1
            return
        if folder.children:
            if "F" in flags:
                delete = True
        else: delete = True
        if delete:
            next(self.repository.delete(folder))
            yield f"Folder deleted: {args[2]}", 0
        else:
            yield f"cannot delete Folder '{args[2]}' because it is not empty", 1
