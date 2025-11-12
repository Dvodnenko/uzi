from dataclasses import fields
from datetime import datetime
from enum import IntEnum

from ..entities import Entity
from ..repositories.folder import saFolderRepository
from ..database.funcs import get_all_by_titles
from ..funcs import is_, cast_datetime


def cast_kwargs(
    model: type[Entity] = Entity,
    exclude: set[str] = {
        "children", "id", "parent", 
        "parent_id", "type"},
):

    def decorator(func):
        def wrap(self, args: list, flags: list, **kwargs):
            allowed = {f for f in fields(model)}.difference(exclude)

            for field in allowed:
                if not field.name in {f.name for f in allowed}\
                    .intersection(k for k in kwargs.keys())\
                    .difference({"links"} # links cannot be parsed here
                ): 
                    continue
                if is_(field.type, datetime):
                    kwargs[field.name] = cast_datetime(kwargs[field.name])
                elif is_(field.type, IntEnum):
                    field.type(int(kwargs[field.name]))

            if kwargs.get("links") is not None:
                if kwargs["links"] == "":
                    kwargs["links"] = []
                else:
                    linksstr: str = kwargs["links"]
                    kwargs["links"] = []
                    gen = get_all_by_titles(
                        self.repository.session,
                        Entity, 
                        linksstr.split(",") if "," in linksstr else [linksstr]
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
