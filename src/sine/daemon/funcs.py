import traceback

import dateparser


def asexc(e: Exception):
    """
    Prints an exception in a pretty way
    """
    
    return " ".join(p for p in traceback.format_exception(e, chain=True))


def cast_datetime(value: str):
    res = dateparser.parse(value)
    if res:
        return res.replace(microsecond=0)
    raise ValueError(f"cannot parse string '{value}'")

def is_(type_: type, other: type):
    return (type_ is other) or (issubclass(type_, other))
