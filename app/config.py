import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings

load_dotenv()


ROOT_DIR = str(Path(os.path.realpath(__file__)).parent.parent.absolute())
RESOURCE_DIR = ROOT_DIR + "/KsdNaverOCRServer/tests/resource/"
sys.path.insert(0, ROOT_DIR)
RESULT_FILE = ROOT_DIR + "/KsdNaverOCRServer/result/"
with open(ROOT_DIR + "/ocr-domain_test_22_03_26_v2.json") as json_file:
    NAVER_OCR_DOMAIN_KEY_LIST = json.load(json_file)
with open(ROOT_DIR + "/general-ocr-domain.json") as json_file:
    GENERAL_OCR_DOMAIN_KEY = json.load(json_file)


class Settings(BaseSettings):
    SECRET_KEY: str = "SECRET_KEY"
    ALGORITHM: str = "ALGORITHM"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    MYSQL_MANAGER_USER: str = "MYSQL_MANAGER_USER"
    MYSQL_MANAGER_PASSWORD: str = "MYSQL_MANAGER_PASSWORD"
    MYSQL_MANAGER_HOST: str = "MYSQL_MANAGER_HOST"
    MYSQL_MANAGER_PORT: int = 3306
    MYSQL_MANAGER_DB: str = "MYSQL_MANAGER_DB"
    MYSQL_MANAGER_CHARSET: str = "MYSQL_MANAGER_CHARSET"
    # database
    DATABASE_HOSTNAME: str = "DATABASE_HOSTNAME"
    DATABASE_CREDENTIALS: str = "DATABASE_CREDENTIALS"
    # this will support special chars for credentials
    _DATABASE_CREDENTIAL_USER, _DATABASE_CREDENTIAL_PASSWORD = str(DATABASE_CREDENTIALS).split(":")  # noqa E501
    DATABASE_NAME: str = "DATABASE_NAME"
    DATABASE_PORT: int = 5432

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=self._DATABASE_CREDENTIAL_USER,
            password=self._DATABASE_CREDENTIAL_PASSWORD,
            host=self.DATABASE_HOSTNAME,
            port=self.DATABASE_PORT,
            path=f"{self.DATABASE_NAME}",
        ).unicode_string()
