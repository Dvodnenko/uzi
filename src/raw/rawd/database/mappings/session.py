from sqlalchemy import Table, Column, Integer, ForeignKey, DateTime, Text

from ..orm_registry import mapping_registry


sessions_table = Table(
    "sessions",
    mapping_registry.metadata,
    Column("id", Integer, ForeignKey("entities.id"), 
           primary_key=True, autoincrement=True),
    Column("start", DateTime, nullable=False),
    Column("end", DateTime, nullable=True),
    Column("summary", Text, nullable=True),
)
