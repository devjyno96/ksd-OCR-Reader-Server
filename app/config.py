import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pydantic import MySQLDsn, computed_field
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

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> MySQLDsn:
        return MySQLDsn.build(
            scheme="mysql+pymysql",
            username=self.MYSQL_MANAGER_USER,
            password=self.MYSQL_MANAGER_PASSWORD,
            host=self.MYSQL_MANAGER_HOST,
            port=self.MYSQL_MANAGER_PORT,
            path=self.MYSQL_MANAGER_DB,
            query=f"charset={self.MYSQL_MANAGER_CHARSET}",
        )
