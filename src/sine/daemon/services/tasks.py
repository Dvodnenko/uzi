from ..repositories.task import saTaskRepository
from ..repositories.folder import saFolderRepository
from ..entities import Task
from ..database.funcs import get_all_by_titles, select
from .decorators import cast_kwargs
from .base import Service
from ...common import load_config, parse_afk, drill, CONFIG_GLOBALS
from ...common.constants import DEFAULT_FMT
from ..funcs import asexc


PARSER = parse_afk
class TaskService(Service):
    def __init__(self, repository: saTaskRepository):
        self.repository = repository
        self.folders_repository = saFolderRepository(repository.session)

    def execute(self, argv):
        if not hasattr(self, argv[0]):
            yield f"Command not found: {argv}", 1
            return
        try:
            if len(argv) > 1:
                args, flags, kwargs = PARSER(argv[1:])
            else:
                args, flags, kwargs = PARSER([])
            gen = getattr(self, argv[0])(args=args, flags=flags, **kwargs)
            yield from gen
        except Exception as e:
            yield asexc(e), 1

    @cast_kwargs(Task)
    def create(self, args: list, flags: list, **kwargs):
        task = Task(**kwargs)
        if next(self.repository.get(task.title)):
            yield f"Task already exists: {task.title}", 1
            return
        next(self.repository.create(task))
        yield f"Task created: {task.title}", 0
    
    def all(self, args: list, flags: list, **kwargs):
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

    def select(self, args: list, flags: list, **kwargs):
        sortby = kwargs.pop("sortby", "title")
        fmt = kwargs.pop("fmt", "0")
        if "t" in flags:
            for task in select(self.repository.session, Task, kwargs, sortby):
                yield task.title, 0
        else:
            config = load_config()
            pattern: str = drill(
                config, ["output", "tasks", "formats", fmt], default=DEFAULT_FMT)
            for task in select(self.repository.session, Task, kwargs, sortby):
                yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": task}), 0
    
    def print(self, args: list, flags: list, **kwargs):
        config = load_config()
        fmt = kwargs.pop("fmt", "0")
        pattern: str = drill(
            config, ["output", "tasks", "formats", fmt], default=DEFAULT_FMT)
        for task in get_all_by_titles(self.repository.session, Task, args):
            yield eval(f"f'{pattern}'", globals={**CONFIG_GLOBALS, "e": task}), 0
    
    @cast_kwargs(Task)
    def update(self, args: list, flags: list, **kwargs):
        current = next(self.repository.get(args[0]))
        if not current:
            yield f"Task not found: {args[0]}", 1
            return
        next(self.repository.update(args[0], **kwargs))
        yield f"Task updated: {args[0]}", 0

    def delete(self, args: list, flags: list, **kwargs):
        task = next(self.repository.get(args[0]))
        if not task:
            yield f"Task not found: {args[0]}", 1
            return
        next(self.repository.delete(task))
        yield f"Task deleted: {args[0]}", 0
