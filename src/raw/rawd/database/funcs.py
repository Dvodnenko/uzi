from sqlalchemy import select

from ..entities import Entity


def get_all_by_titles(
    session, model, titles: list[str]
) -> list[Entity]:
        query = select(model) \
            .where(model.title.in_(titles))
        objs = session.scalars(query).unique().all()
        return objs
