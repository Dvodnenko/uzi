from ..repositories.folder import saFolderRepository
from ..entities import Folder
from ..database.funcs import get_all_by_titles
from .decorators import cast_kwargs
from .base import Service
from ...common import load_config, parse_afk
from ..funcs import asexc


PARSER = parse_afk
class FolderService(Service):

    def __init__(self, repository: saFolderRepository):
        self.repository = repository

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

    @cast_kwargs(Folder)
    def create(self, args: list, flags: list, **kwargs):
        folder = Folder(**kwargs)
        if next(self.repository.get(folder.title)):
            yield f"Folder already exists: {folder.title}", 1
            return
        next(self.repository.create(folder))
        yield f"Folder created: {folder.title}", 0
    
    def all(self, args: list, flags: list, **kwargs):
        sortby = kwargs.get("sortby", "title")
        if "t" in flags:
            for folder in self.repository.get_all(sortby):
                yield folder.title, 0
        else:
            pattern: str = load_config()["formats"]["folder"]
            for folder in self.repository.get_all(sortby):
                yield pattern.format(**folder.to_dict()), 0
    
    def print(self, args: list, flags: list, **kwargs):
        pattern: str = load_config()["formats"]["folder"]
        for folder in get_all_by_titles(self.repository.session, Folder, args):
            yield pattern.format(**folder.to_dict()), 0

    @cast_kwargs(Folder)
    def update(self, args: list, flags: list, **kwargs):
        current = next(self.repository.get(args[0]))
        if not current:
            yield f"Folder not found: {args[0]}", 1
        next(self.repository.update(args[0], **kwargs))
        yield f"Folder updated: {args[0]}", 0

    def delete(self, args: list, flags: list, **kwargs):
        folder = next(self.repository.get(args[0]))
        delete = False
        if not folder:
            yield f"Folder not found: {args[0]}", 1
            return
        if folder.children:
            if "F" in flags:
                delete = True
        else: delete = True
        if delete:
            next(self.repository.delete(folder))
            yield f"Folder deleted: {args[0]}", 0
        else:
            yield f"cannot delete Folder '{args[0]}' because it is not empty", 1
