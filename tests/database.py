from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app.config import settings

test_engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
TestingSession = scoped_session(TestingSessionLocal)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
