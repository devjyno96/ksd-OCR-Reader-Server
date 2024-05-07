from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = create_engine(
    url=settings.SQLALCHEMY_DATABASE_URI,
)

SessionLocal = sessionmaker(bind=engine)
SessionLocal.configure(bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
