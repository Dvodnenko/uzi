from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class Folder(Base):
    __tablename__ = "folders"

    id: Mapped[int] = mapped_column(
        ForeignKey("entities.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "folder",
    }
