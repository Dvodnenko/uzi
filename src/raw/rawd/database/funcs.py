from sqlalchemy import select


def get_all_by_titles(session, model, titles: list[str]):
        query = select(model) \
            .where(model.title.in_(titles))
        for obj in session.scalars(query).unique().yield_per(10):
            yield obj
