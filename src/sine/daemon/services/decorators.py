from dataclasses import fields
from datetime import datetime
from enum import IntEnum

import dateparser

from ..entities import Entity
from ..repositories.folder import saFolderRepository
from ..database.funcs import get_all_by_titles


def cast_datetime(value: str):
    return (dateparser.parse(value) or \
        datetime.now()).replace(microsecond=0)

def is_(type_: type, other: type):
    return (type_ is other) or (issubclass(type_, other))


def cast_kwargs(
    model: type[Entity] = Entity,
    exclude: set[str] = {},
):

    def decorator(func):
        def wrap(self, args: list, flags: list, **kwargs):
            allowed = {f for f in fields(model)}

            for field in allowed:
                if not field.name in {f.name for f in allowed}\
                    .intersection(k for k in kwargs.keys())\
                    .difference(exclude):
                    continue
                if is_(field.type, datetime):
                    kwargs[field.name] = cast_datetime(kwargs[field.name])
                elif is_(field.type, IntEnum):
                    field.type(int(kwargs[field.name]))

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
