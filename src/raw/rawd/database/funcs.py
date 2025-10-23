from sqlalchemy import select

from ..entities import Entity
from .session import engine


def get_all_by_titles(
    model, titles: list[str]
) -> list[Entity]:
    with engine.connect() as conn:
        query = select(model) \
            .where(model.title.in_(titles))
        objs = conn.scalars(query).unique().all()
        return objs
