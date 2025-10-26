from datetime import datetime
from dataclasses import fields

from ..entities import Entity, Color
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
            if kwargs.get("links"):
                if kwargs["links"] == "":
                    kwargs["links"] = []
                else:
                    kwargs["links"] = get_all_by_titles(
                        Entity, 
                        kwargs["links"].split(",")
                    )
            if kwargs.get("start"):
                kwargs["start"] = datetime.fromisoformat(
                    kwargs["start"]).replace(microsecond=0)
            if kwargs.get("end"):
                kwargs["end"] = datetime.fromisoformat(
                    kwargs["end"]).replace(microsecond=0)
            if kwargs.get("title"):
                title = kwargs.get("title")
                kwargs["title"] = title
                parentstr = title[0:title.rfind("/")]
                if parentstr != "": # has parent
                    local_folder_repo = saFolderRepository(
                        self.repository.session)
                    parent = local_folder_repo.get(
                        parentstr)
                    if not parent:
                        return f"Folder not found: {parentstr}", 1
                    kwargs["parent"] = parent
                
            return func(self, args, flags, **kwargs)
        return wrap
    return decorator


CONFIG = load_config()


def provide_conf(func):

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs, __cnf=CONFIG)
    
    return wrapper

