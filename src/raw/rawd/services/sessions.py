from datetime import datetime

from ..repositories.session import saSessionRepository
from ..repositories.folder import saFolderRepository
from ..entities import Session
from ..database.funcs import get_all_by_titles
from .decorators import provide_conf, cast_kwargs


class SessionService:
    def __init__(self, repository: saSessionRepository):
        self.repository = repository
        self.folders_repository = saFolderRepository(repository.session)
        self.active: Session | None = None

    @cast_kwargs(Session)
    def begin(self, args: list, flags: list, **kwargs):
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
    def stop(self, args: list, flags: list, **kwargs):
        session = next(self.repository.get_active())
        if not session:
            yield "Active Session not found", 1
            return
        kwargs["end"] = kwargs.get("end",
            datetime.now().replace(microsecond=0))
        next(self.repository.update(session.title, **kwargs))
        yield "Session stoped", 0
    
    @provide_conf
    def all(self, args: list, flags: list, **kwargs):
        sortby = kwargs.get("sortby", "title")
        if "t" in flags:
            for session in self.repository.get_all(sortby):
                yield session.title, 0
        else:
            pattern: str = kwargs["__cnf"]["formats"]["session"]
            for session in self.repository.get_all(sortby):
                yield pattern.format(**session.to_dict()), 0
    
    @provide_conf
    def print(self, args: list, flags: list, **kwargs):
        pattern: str = kwargs["__cnf"]["formats"]["session"]
        for session in get_all_by_titles(self.repository.session, Session, args):
            yield pattern.format(**session.to_dict()), 0
    
    @cast_kwargs(Session)
    def update(self, args: list, flags: list, **kwargs):
        current = next(self.repository.get(args[0]))
        if not current:
            yield f"Session not found: {args[0]}", 1
            return
        next(self.repository.update(args[0], **kwargs))
        yield f"Session updated: {args[0]}", 0

    def delete(self, args: list, flags: list, **kwargs):
        session = next(self.repository.get(args[0]))
        if not session:
            yield f"Session not found: {args[0]}", 1
            return
        next(self.repository.delete(session))
        yield f"Session deleted: {args[0]}", 0
