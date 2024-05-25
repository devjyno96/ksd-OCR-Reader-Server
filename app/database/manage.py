from sqlalchemy_utils import create_database, database_exists

from app.config import settings
from app.database.core import Base, engine


def get_tables():
    tables = []
    for _, table in Base.metadata.tables.items():
        tables.append(table)
    return tables


def init_database():
    """Initializes the database."""
    if not database_exists(str(settings.SQLALCHEMY_DATABASE_URI)):
        create_database(str(settings.SQLALCHEMY_DATABASE_URI))

    tables = get_tables()

    Base.metadata.create_all(engine, tables=tables)


def delete_all():
    """
    delete all defined tables
    """
    Base.metadata.drop_all(bind=engine)
