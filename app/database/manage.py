from app.database.core import Base
from app.database.manage import engine


def create_all():
    """
    create all defined tables
    """
    Base.metadata.create_all(bind=engine)


def delete_all():
    """
    delete all defined tables
    """
    Base.metadata.drop_all(bind=engine)
