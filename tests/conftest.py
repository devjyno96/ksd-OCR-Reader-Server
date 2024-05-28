import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, drop_database

from app.database.core import get_db
from app.database.manage import init_database
from tests.database import TestingSession, override_get_db, test_engine


@pytest.fixture(scope="session")
def db():
    if database_exists(test_engine.url):
        drop_database(test_engine.url)

    init_database()
    yield
    drop_database(test_engine.url)


@pytest.fixture(scope="function", autouse=True)
def session(db) -> Session:  # type: ignore
    """
    Creates a new database session with (with working transaction)
    for test duration.
    """
    session = TestingSession()
    session.begin_nested()
    yield session
    session.rollback()


@pytest.fixture(scope="session")
def testapp():
    from app.main import app

    yield app


@pytest.fixture(scope="function")
def client(testapp, session) -> TestClient:  # type: ignore
    testapp.dependency_overrides[get_db] = override_get_db
    yield TestClient(testapp)
