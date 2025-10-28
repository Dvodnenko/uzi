from sqlalchemy import select
from sqlalchemy.orm import Session as ormSession

from ..entities import Tag
from ..database.session import transaction


class saTagRepository:
    def __init__(self, session: ormSession):
        self.session = session

    @transaction
    def create(self, tag: Tag) -> None:
        self.session.add(tag)
        return None

    def get(self, title: str) -> Tag | None:
        query = select(Tag) \
            .where(Tag.title == title)
        obj = self.session.scalars(query).first()
        return obj

    def get_all(self) -> list[Tag]:
        query = select(Tag)
        tags = self.session.scalars(query).unique().all()
        return tags

    @transaction
    def update(self, title_: str, **kwargs) -> None:
        tag = (self.session.query(Tag)
                  .filter_by(title=title_)
                  .first())
        tag = tag.update(**kwargs)
        return None

    @transaction
    def delete(self, entity: Tag) -> None:
        self.session.delete(entity)
        return None
