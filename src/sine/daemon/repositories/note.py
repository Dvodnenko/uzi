from sqlalchemy import select
from sqlalchemy.orm import Session as ormSession

from ..entities import Note


class saNoteRepository:
    def __init__(self, session: ormSession):
        self.session = session

    def create(self, note: Note):
        self.session.add(note)
        self.session.commit()
        yield

    def get(self, title: str):
        query = select(Note) \
            .where(Note.title == title)
        obj = self.session.scalars(query).first()
        yield obj

    def get_all(self, order_by: str = "title"):
        batch_size = 100
        offset = 0
        while True:
            batch = self.session.query(Note).order_by(getattr(Note, order_by)).\
                limit(batch_size).offset(offset).all()
            if not batch:
                break
            for obj in batch:
                yield obj
            offset += batch_size

    def update(self, title_: str, **kwargs):
        note = (self.session.query(Note)
                  .filter_by(title=title_)
                  .first())
        note = note.update(**kwargs)
        self.session.commit()
        yield

    def delete(self, entity: Note):
        self.session.delete(entity)
        self.session.commit()
        yield
