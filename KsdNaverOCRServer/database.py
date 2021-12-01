from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from KsdNaverOCRServer import config


def create_sqlite_db_engine():
    SQLALCHAMY_DATABASE_URL = f'sqlite:////{config.ROOT_DIR}/ocr-server.db'

    # Test code 에서도 사용하기 때문에 절대 경로로 지정해 준다
    return create_engine(SQLALCHAMY_DATABASE_URL, connect_args={"check_same_thread": False}, pool_pre_ping=True)


def create_mysql_db_engine():
    db_username = config.MYSQL_MANAGER_USER
    db_password = config.MYSQL_MANAGER_PASSWORD
    db_host = config.MYSQL_MANAGER_HOST
    db_dbname = config.MYSQL_MANAGER_DB
    db_charset = config.MYSQL_MANAGER_CHARSET

    MYSQL_DATABASE_URL = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_dbname}?charset={db_charset}"

    return create_engine(MYSQL_DATABASE_URL, pool_pre_ping=True)


print(config.ROOT_DIR)
DATABASE_TYPE = 'MYSQL'
DATABASE_TYPE = 'SQLITE'

if DATABASE_TYPE == 'SQLITE':
    engine = create_sqlite_db_engine()
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, )


    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

elif DATABASE_TYPE == 'MYSQL':
    engine = create_mysql_db_engine()
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, )

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
