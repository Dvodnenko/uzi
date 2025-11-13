import re
from typing import Callable, Any


ARG_RE = re.compile(r'(?<!\S)(?!-)[^\s]+')

def drill(
    dict_: dict,
    path: list,
    pattern: re.Pattern = None,
    conditions: list[Callable[[Any], bool]] = [lambda *args, **kwargs: True],
    default = None,
    raise_: bool = False
):
    result = dict_
    if pattern:
        path = pattern.findall(" ".join(p for p in path))
    try:
        for p in path:
            result = result[p]
        if all([condition(result) for condition in conditions]):
            return result
        elif raise_: raise KeyError(f"no such value: {path}")
        return default
    except KeyError:
        return default
