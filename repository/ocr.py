import sqlalchemy
from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session

# from ..models import test as test_models

# from ..schemas import admin_dashboard as admin_dashboard_schemas

import requests
import time
import json

NAVER_OCR_URL = "312ab1aaaad04cb4907e2bdfb246bc67.apigw.ntruss.com/custom/v1/3870/40d9e6658a8a7c8b7d764aa349b635ea318d81480956aa066bccd98e5a61f074"
NAVER_OCR_SECRET = "VXdEdFJDZ2lrWWdRZ2FmYUpWV25SWWVaT0VuZFNPU2Y="


def ocr_request(s3_url: str, ocr_type: str):
    print(ocr_type)
    request_json = {
        'images': [
            {
                'format': s3_url.split('.')[-1],
                'name': 'image',
                'url': s3_url
            }
        ],
        'requestId': 'ocr-request',
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = json.dumps(request_json).encode('UTF-8')
    headers = {
        'X-OCR-SECRET': NAVER_OCR_SECRET,
        'Content-Type': 'application/json'
    }

    return json.dumps(
        requests.request("POST", 'https://{}/infer'.format(NAVER_OCR_URL), headers=headers, data=payload).json(),
        ensure_ascii=False)
