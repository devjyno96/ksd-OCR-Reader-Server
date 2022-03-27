import json
import sys
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

ROOT_DIR = str(Path(os.path.realpath(__file__)).parent.parent.absolute())


RESOURCE_DIR = ROOT_DIR + "/KsdNaverOCRServer/tests/resource/"

sys.path.insert(0, ROOT_DIR)
RESULT_FILE = ROOT_DIR + "/KsdNaverOCRServer/result/"
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

with open(ROOT_DIR + "/ocr-domain_test_22_03_26_v2.json") as json_file:
# with open(ROOT_DIR + "/ocr-domain.json") as json_file:
    NAVER_OCR_DOMAIN_KEY_LIST = json.load(json_file)
with open(ROOT_DIR + "/general-ocr-domain.json") as json_file:
    GENERAL_OCR_DOMAIN_KEY = json.load(json_file)

MYSQL_MANAGER_USER = os.getenv('MYSQL_MANAGER_USER')
MYSQL_MANAGER_PASSWORD = os.getenv('MYSQL_MANAGER_PASSWORD')
MYSQL_MANAGER_HOST = os.getenv('MYSQL_MANAGER_HOST')
MYSQL_MANAGER_DB = os.getenv('MYSQL_MANAGER_DB')
MYSQL_MANAGER_CHARSET = os.getenv('MYSQL_MANAGER_CHARSET')
