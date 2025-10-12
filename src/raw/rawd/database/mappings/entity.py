from typing import Optional

from sqlalchemy import Integer, String, UniqueConstraint, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base
from ...enums.color import Color


class Entity(Base):
    __tablename__ = "entities"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    color: Mapped[Color] = mapped_column(
        Enum(Color, name="color_enum", create_type=True), 
        default=Color.WHITE, nullable=False)
    type: Mapped[str] = mapped_column(String)
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("entities.id"), default=None)

    parent: Mapped[Optional["Entity"]] = relationship(
        back_populates="children", remote_side=[id])
    children: Mapped[list["Entity"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan")

    __mapper_args__ = {
        "polymorphic_identity": "entity",
        "polymorphic_on": type,
        "with_polymorphic": "*",
    }
    __table_args__ = (
        UniqueConstraint("title", "type", name="uq_title_n_type")
    )
