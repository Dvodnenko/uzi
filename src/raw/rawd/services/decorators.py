from dataclasses import fields

from ..entities import Entity, Color, TaskStatus
from ..repositories.folder import saFolderRepository
from ..database.funcs import get_all_by_titles
from ...config import load_config


def cast_kwargs(
    model: type[Entity] = Entity,
    exclude: set[str] = {},
):

    def decorator(func):
        def wrap(self, args: list, flags: list, **kwargs):
            allowed = {f.name for f in fields(model)}
            kwargs = {key: kwargs[key] 
                               for key in allowed.\
                                intersection(kwargs.keys()).\
                                difference(exclude)}

            if kwargs.get("color"):
                kwargs["color"] = Color(
                    int(kwargs["color"]))
            if kwargs.get("status"):
                kwargs["status"] = TaskStatus(
                    int(kwargs["status"]))
            if kwargs.get("links"):
                if kwargs["links"] == "":
                    ...
                else:
                    linksstr: str = kwargs["links"]
                    kwargs["links"] = []
                    gen = get_all_by_titles(
                        self.repository.session,
                        Entity, 
                        linksstr.split(",")
                    )
                    for link in gen:
                        kwargs["links"].append(link)
            if kwargs.get("title"):
                title = kwargs.get("title")
                kwargs["title"] = title
                parentstr = title[0:title.rfind("/")]
                if parentstr != "": # has parent
                    local_folder_repo = saFolderRepository(
                        self.repository.session)
                    parent = next(local_folder_repo.get(parentstr))
                    if not parent:
                        yield f"Folder not found: {parentstr}", 1
                        return
                    kwargs["parent"] = parent
                
            yield from func(self, args, flags, **kwargs)
        return wrap
    return decorator


CONFIG = load_config()


def provide_conf(func):

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs, __cnf=CONFIG)
    
    return wrapper
