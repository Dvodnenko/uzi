from typing import TypeVar, Any, Generator
from dataclasses import fields
from datetime import datetime

from sqlalchemy import select as _select
from sqlalchemy.orm import selectinload, Session

from ..funcs import cast_datetime


def get_all_by_titles(session, model, titles: list[str]):
        query = _select(model) \
            .where(model.title.in_(titles))
        for obj in session.scalars(query).unique().yield_per(10):
            yield obj


OPERATORS = {
    "eq": lambda col, val: col == val,
    "ne": lambda col, val: col != val,
    "gt": lambda col, val: col > val,
    "lt": lambda col, val: col < val,
    "ge": lambda col, val: col >= val,
    "le": lambda col, val: col <= val,
    "contains": lambda col, val: col.like(f"%{val}%"),
    "notcontains": lambda col, val: col.notlike(f"%{val}%"),
    "icontains": lambda col, val: col.ilike(f"%{val}%"),
    "noticontains": lambda col, val: col.notilike(f"%{val}%"),
    "in": lambda col, val: col.in_(val if isinstance(val, list) else [val]),
    "notin": lambda col, val: col.notin_(val if isinstance(val, list) else [val]),
}

def apply_filters(query, model, filters: dict):
    simple_kwargs = {}
    complex_expressions = []
    allowed = {f.name: f for f in fields(model)}

    for key, value in filters.items():
        if "__" in key:
            field, op = key.split("__", 1)
            if not hasattr(model, field):
                continue
            if allowed[field].type is datetime:
                value = cast_datetime(value)
            column = getattr(model, field)
            if op in OPERATORS:
                expr = OPERATORS[op](column, value)
                complex_expressions.append(expr)
        else:
            simple_kwargs[key] = value

    if simple_kwargs:
        query = query.filter_by(**simple_kwargs)

    if complex_expressions:
        query = query.filter(*complex_expressions)

    return query


T_ = TypeVar("T", bound=Any)

def filter(
    session: Session,
    model: type[T_],
    filters: dict, 
    order_by: str
) -> Generator[T_, Any, None]:
    query = session.query(model).options(
        selectinload(model.links)
    ).order_by(getattr(model, order_by))
    query = apply_filters(query, model, filters)
    for obj in query.yield_per(10):
        yield obj
