import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.insert(0, ROOT_DIR)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


with open(ROOT_DIR + "/ocr-domain.json") as json_file:
    NAVER_OCR_DOMAIN_KEY_LIST = json.load(json_file)

