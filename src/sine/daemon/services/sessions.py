from datetime import datetime

from ..repositories.session import saSessionRepository
from ..repositories.folder import saFolderRepository
from ..entities import Session
from ..database.funcs import get_all_by_titles, filter
from .decorators import cast_kwargs
from .base import Service
from ...common import load_config, drill, CONFIG_GLOBALS
from ...common.constants import DEFAULT_FMT
from ..funcs import asexc


class SessionService(Service):
    def __init__(self, repository: saSessionRepository):
        self.repository = repository
        self.folders_repository = saFolderRepository(repository.session)
        self.active: Session | None = None

    def execute(self, rspd):
        if not hasattr(self, rspd["source"][1]):
            yield f"Command not found: {rspd["source"][1]}", 1
            return
        try:
            gen = getattr(self, rspd["source"][1])(rspd)
            yield from gen
        except Exception as e:
            yield asexc(e), 1

    @cast_kwargs(Session)
    def begin(self, rspd: dict):
        _, _, kwargs = rspd["ps"]["afk"]
        if not kwargs.get("styles") and kwargs.get("parent"):
            kwargs["styles"] = kwargs["parent"].styles
        active = next(self.repository.get_active())
        if active:
            yield f"Session is already started: '{active.title}'", 1
            return
        kwargs["start"] = kwargs.get("start", 
            datetime.now().replace(microsecond=0))
        session = Session(**kwargs)
        next(self.repository.create(session))
        yield f"Session started", 0
    
    @cast_kwargs(Session)
    def stop(self, rspd: dict):
        _, _, kwargs = rspd["ps"]["afk"]
        session = next(self.repository.get_active())
        if not session:
            yield "Active Session not found", 1
            return
        kwargs["end"] = kwargs.get("end",
            datetime.now().replace(microsecond=0))
        next(self.repository.update(session.title, **kwargs))
        yield "Session stoped", 0
    
    def all(self, rspd: dict):
        _, flags, kwargs = rspd["ps"]["afk"]
        sortby = kwargs.get("sortby", "title")
        if "t" in flags:
            for session in self.repository.get_all(sortby):
                yield session.title, 0
        else:
            config = load_config()
            fmt = kwargs.get("fmt", "0")
            pattern: str = drill(
                config, ["output", "sessions", "formats", fmt], default=DEFAULT_FMT)
            for session in self.repository.get_all(sortby):
                yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": session}), 0

    def filter(self, rspd: dict):
        _, flags, kwargs = rspd["ps"]["afk"]
        filters = rspd["ps"]["sql"]
        sortby = kwargs.pop("sortby", "title")
        fmt = kwargs.pop("fmt", "0")
        if "t" in flags:
            for session in filter(self.repository.session, Session, filters, sortby):
                yield session.title, 0
        else:
            config = load_config()
            pattern: str = drill(
                config, ["output", "sessions", "formats", fmt], default=DEFAULT_FMT)
            for session in filter(self.repository.session, Session, filters, sortby):
                yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": session}), 0
    
    def print(self, rspd: dict):
        args, _, kwargs = rspd["ps"]["afk"]
        config = load_config()
        fmt = kwargs.pop("fmt", "0")
        pattern: str = drill(
            config, ["output", "sessions", "formats", fmt], default=DEFAULT_FMT)
        for session in get_all_by_titles(self.repository.session, Session, args):
            yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": session}), 0
    
    @cast_kwargs(Session)
    def update(self, rspd: dict):
        args, _, kwargs = rspd["ps"]["afk"]
        current = next(self.repository.get(args[2]))
        if not current:
            yield f"Session not found: {args[2]}", 1
            return
        next(self.repository.update(args[2], **kwargs))
        yield f"Session updated: {args[2]}", 0

    def delete(self, rspd: dict):
        args, _, _ = rspd["ps"]["afk"]
        session = next(self.repository.get(args[2]))
        if not session:
            yield f"Session not found: {args[2]}", 1
            return
        next(self.repository.delete(session))
        yield f"Session deleted: {args[2]}", 0
