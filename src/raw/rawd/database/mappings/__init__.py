from sqlalchemy.orm import relationship

from ..orm_registry import mapping_registry
from ...entities import Entity, Folder, Session
from .entity import entities_table, entity_links_table
from .folder import folders_table
from .session import sessions_table


def map_entities_table():
    mapping_registry.map_imperatively(
        Entity,
        entities_table,
        polymorphic_on=entities_table.c.type,
        polymorphic_identity="entity",
        properties={
            "links": relationship(
                "Entity",
                secondary=entity_links_table,
                primaryjoin=entities_table.c.id == entity_links_table.c.entity_id,
                secondaryjoin=entities_table.c.id == entity_links_table.c.link_id,
                lazy="joined",
            ),
            "parent": relationship(
                "Folder", back_populates="children",
                foreign_keys=[entities_table.c.parent_id]
            )
        }
    )

def map_folders_table():
    mapping_registry.map_imperatively(
        Folder, folders_table, inherits=Entity, 
        polymorphic_identity="folder",
        inherit_condition=folders_table.c.id == entities_table.c.id,
        inherit_foreign_keys=[folders_table.c.id],
        properties={
            "children": relationship(
                "Entity",
                back_populates="parent",
                cascade="all, delete-orphan",
                foreign_keys=[entities_table.c.parent_id]
            ),
        }
    )

def map_sessions_table():
    mapping_registry.map_imperatively(
        Session, sessions_table, inherits=Entity, 
        polymorphic_identity="session",
    )


def map_tables():
    map_entities_table()
    map_folders_table()
    map_sessions_table()
