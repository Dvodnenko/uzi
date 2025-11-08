from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

from ...common.config import load_config
from .orm_registry import mapping_registry
from .mappings import map_tables


conf = load_config()
engine = create_engine(
    url=f"sqlite:///{conf.get("data_file_path")}",
    echo=conf.get("echo"),
)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)


def init_db():
    mapping_registry.metadata.create_all(bind=engine)
    map_tables()

    with engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys = ON;"))
