import json
import os
import sys
from pathlib import Path

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = str(Path(os.path.realpath(__file__)).parent.parent.absolute())
RESOURCE_DIR = ROOT_DIR + "/KsdNaverOCRServer/tests/resource/"
sys.path.insert(0, ROOT_DIR)
RESULT_FILE = ROOT_DIR + "/KsdNaverOCRServer/result/"
with open(ROOT_DIR + "/ocr-domain_test_22_03_26_v2.json") as json_file:
    NAVER_OCR_DOMAIN_KEY_LIST = json.load(json_file)
with open(ROOT_DIR + "/general-ocr-domain.json") as json_file:
    GENERAL_OCR_DOMAIN_KEY = json.load(json_file)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    SECRET_KEY: str = "SECRET_KEY"
    ALGORITHM: str = "ALGORITHM"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Admin
    PASSWORD: str = "PASSWORD"
    # database
    DATABASE_HOSTNAME: str = "DATABASE_HOSTNAME"
    DATABASE_CREDENTIALS: str = "DATABASE_CREDENTIALS"
    DATABASE_NAME: str = "DATABASE_NAME"
    DATABASE_PORT: int = 5432

    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        _DATABASE_CREDENTIAL_USER, _DATABASE_CREDENTIAL_PASSWORD = str(self.DATABASE_CREDENTIALS).split(":")  # noqa E501
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=_DATABASE_CREDENTIAL_USER,
            password=_DATABASE_CREDENTIAL_PASSWORD,
            host=self.DATABASE_HOSTNAME,
            port=self.DATABASE_PORT,
            path=f"{self.DATABASE_NAME}",
        ).unicode_string()


settings = Settings()
