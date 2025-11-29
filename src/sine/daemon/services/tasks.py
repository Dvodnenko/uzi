from ..repositories.task import saTaskRepository
from ..repositories.folder import saFolderRepository
from ..entities import Task
from ..database.funcs import get_all_by_titles, filter
from .decorators import cast_kwargs
from .base import Service
from ...common import load_config, drill, CONFIG_GLOBALS
from ...common.constants import DEFAULT_FMT
from ..funcs import asexc


class TaskService(Service):
    def __init__(self, repository: saTaskRepository):
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

    @cast_kwargs(Task)
    def create(self, rspd: dict):
        _, _, kwargs = rspd["ps"]["afk"]
        if not kwargs.get("styles") and kwargs.get("parent"):
            kwargs["styles"] = kwargs["parent"].styles
        task = Task(**kwargs)
        if next(self.repository.get(task.title)):
            yield f"Task already exists: {task.title}", 1
            return
        next(self.repository.create(task))
        yield f"Task created: {task.title}", 0
    
    def all(self, rspd: dict):
        _, flags, kwargs = rspd["ps"]["afk"]
        sortby = kwargs.pop("sortby", "title")
        if "t" in flags:
            for task in self.repository.get_all(sortby):
                yield task.title, 0
        else:
            config = load_config()
            fmt = kwargs.get("fmt", "0")
            pattern: str = drill(
                config, ["output", "tasks", "formats", fmt], default=DEFAULT_FMT)
            for task in self.repository.get_all(sortby):
                yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": task}), 0

    def filter(self, rspd: dict):
        _, flags, kwargs = rspd["ps"]["afk"]
        filters = rspd["ps"]["sql"]
        sortby = kwargs.pop("sortby", "title")
        fmt = kwargs.pop("fmt", "0")
        if "t" in flags:
            for task in filter(self.repository.session, Task, filters, sortby):
                yield task.title, 0
        else:
            config = load_config()
            pattern: str = drill(
                config, ["output", "tasks", "formats", fmt], default=DEFAULT_FMT)
            for task in filter(self.repository.session, Task, filters, sortby):
                yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": task}), 0
    
    def print(self, rspd: dict):
        args, _, kwargs = rspd["ps"]["afk"]
        config = load_config()
        fmt = kwargs.pop("fmt", "0")
        pattern: str = drill(
            config, ["output", "tasks", "formats", fmt], default=DEFAULT_FMT)
        for task in get_all_by_titles(self.repository.session, Task, args):
            yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": task}), 0
    
    @cast_kwargs(Task)
    def update(self, rspd: dict):
        args, _, kwargs = rspd["ps"]["afk"]
        current = next(self.repository.get(args[2]))
        if not current:
            yield f"Task not found: {args[2]}", 1
            return
        next(self.repository.update(args[2], **kwargs))
        yield f"Task updated: {args[2]}", 0

    def delete(self, rspd: dict):
        args, _, _ = rspd["ps"]["afk"]
        task = next(self.repository.get(args[2]))
        if not task:
            yield f"Task not found: {args[2]}", 1
            return
        next(self.repository.delete(task))
        yield f"Task deleted: {args[2]}", 0
