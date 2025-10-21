from sqlalchemy import select

from ..repositories.folder import saFolderRepository
from ..entities import Folder, Entity
from ..database.session import Session
from ..database.funcs import get_all_by_titles


class FolderService:
    def __init__(self):
        self.repository = saFolderRepository(Session())

    def create(self, args: list, flags: list, **kwargs) -> tuple[str, int]:
        links = kwargs.get("links")
        if links:
            links_list = links.split(",")
            query = select(Entity).where(Entity.title.in_(links_list))
            entities = self.repository.session.scalars(query).unique().all()
            kwargs["links"] = entities
        folder = Folder(**kwargs)
        if self.repository.get(folder.title):
            return f"Folder already exists: {folder.title}", 1
        if folder.parentstr != "":
            if not self.repository.get(folder.parentstr):
                return f"Folder not found: {folder.parentstr}", 1
        self.repository.create(folder)
        return f"Folder created: {folder.title}", 0
    
    def all(self, args: list, flags: list, **kwargs):
        sortby = kwargs.get("sortby", "title")
        folders = self.repository.get_all()
        folders = sorted(
            folders,
            key=lambda f: getattr(f, sortby),
            reverse="r" in flags
        )
        return "".join(f"{f.title}\n" for f in folders)[:-1], 0
    
    def print(self, args: list, flags: list, **kwargs):
        folders = get_all_by_titles(self.repository.session, Folder, args)
        return "".join(f"{f.title}\n" for f in folders)[:-1], 0
        
    def update(self, args: list, flags: list, **kwargs):
        links = kwargs.get("links")
        if "links" in kwargs.keys():
            if links is "":
                kwargs["links"] = []
            else:
                links_list = links.split(",")
                query = select(Entity).where(Entity.title.in_(links_list))
                entities = self.repository.session.scalars(query).unique().all()
                kwargs["links"] = entities
        current = self.repository.get(args[0])
        if not current:
            return f"Folder not found: {args[0]}", 1
        self.repository.update(args[0], **kwargs)
        return f"Folder updated: {args[0]}", 0

    def delete(self, args: list, flags: list, **kwargs):
        folder = self.repository.get(args[0])
        delete = False
        if not folder:
            return f"Folder not found: {args[0]}", 1
        if folder.children:
            if "F" in flags:
                delete = True
        else: delete = True
        if delete:
            self.repository.delete(folder)
            return f"Folder deleted: {args[0]}", 0
        else:
            return (f"cannot delete Folder '{args[0]}' because it is not empty"), 1
