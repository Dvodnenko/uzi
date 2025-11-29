from ..repositories.note import saNoteRepository
from ..repositories.folder import saFolderRepository
from ..entities import Note
from ..database.funcs import get_all_by_titles, filter
from .decorators import cast_kwargs
from .base import Service
from ...common import load_config, drill, CONFIG_GLOBALS
from ...common.constants import DEFAULT_FMT
from ..funcs import asexc


class NoteService(Service):
    def __init__(self, repository: saNoteRepository):
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

    @cast_kwargs(Note)
    def create(self, rspd: dict):
        _, _, kwargs = rspd["ps"]["afk"]
        if not kwargs.get("styles") and kwargs.get("parent"):
            kwargs["styles"] = kwargs["parent"].styles
        note = Note(**kwargs)
        if next(self.repository.get(note.title)):
            yield f"Note already exists: {note.title}", 1
            return
        next(self.repository.create(note))
        yield f"Note created: {note.title}", 0
    
    def all(self, rspd: dict):
        _, flags, kwargs = rspd["ps"]["afk"]
        sortby = kwargs.pop("sortby", "title")
        if "t" in flags:
            for note in self.repository.get_all(sortby):
                yield note.title, 0
        else:
            config = load_config()
            fmt = kwargs.get("fmt", "0")
            pattern: str = drill(
                config, ["output", "notes", "formats", fmt], default=DEFAULT_FMT)
            for note in self.repository.get_all(sortby):
                yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": note}), 0

    def filter(self, rspd: dict):
        _, flags, kwargs = rspd["ps"]["afk"]
        filters = rspd["ps"]["sql"]
        sortby = kwargs.pop("sortby", "title")
        fmt = kwargs.pop("fmt", "0")
        if "t" in flags:
            for note in filter(self.repository.session, Note, filters, sortby):
                yield note.title, 0
        else:
            config = load_config()
            pattern: str = drill(
                config, ["output", "notes", "formats", fmt], default=DEFAULT_FMT)
            for note in filter(self.repository.session, Note, filters, sortby):
                yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": note}), 0
    
    def print(self, rspd: dict):
        args, _, kwargs = rspd["ps"]["afk"]
        config = load_config()
        fmt = kwargs.pop("fmt", "0")
        pattern: str = drill(
            config, ["output", "notes", "formats", fmt], default=DEFAULT_FMT)
        for note in get_all_by_titles(self.repository.session, Note, args):
            yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": note}), 0
    
    @cast_kwargs(Note)
    def update(self, rspd: dict):
        args, _, kwargs = rspd["ps"]["afk"]
        current = next(self.repository.get(args[2]))
        if not current:
            yield f"Note not found: {args[2]}", 1
            return
        next(self.repository.update(args[2], **kwargs))
        yield f"Note updated: {args[2]}", 0

    def delete(self, rspd: dict):
        args, _, _ = rspd["ps"]["afk"]
        note = next(self.repository.get(args[2]))
        if not note:
            yield f"Note not found: {args[2]}", 1
            return
        next(self.repository.delete(note))
        yield f"Note deleted: {args[2]}", 0
