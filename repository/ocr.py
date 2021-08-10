import sqlalchemy
from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session

# from ..models import test as test_models

from schemas import ocr as ocr_schemas

import requests
import time
import json

from resources.naver_ocr_domain_key import NAVER_OCR_DOMAIN_KEY as ocr_keys


def ocr_request(request: ocr_schemas.RequestOCR):
    selected_ocr = ocr_keys[0]
    for ocr_key in ocr_keys:
        if ocr_key['category'] == request.ocr_type:
            selected_ocr = ocr_key
    request_json = {
        'images': [
            {
                'format': request.s3_url.split('.')[-1],
                'name': 'image',
                'url': request.s3_url
            }
        ],
        'requestId': 'ocr-request',
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }

    payload = json.dumps(request_json).encode('UTF-8')
    headers = {
        'X-OCR-SECRET': selected_ocr['secret_key'],
        'Content-Type': 'application/json'
    }

    response = requests.post(url=selected_ocr['APIGW_Invoke_url'], headers=headers, data=payload)
    # print_result_on_terminal(response)
    return json.loads(response.text)


def print_result_on_terminal(response):
    dict_data = json.loads(response.text)
    if dict_data['images'][0]['inferResult'] == 'SUCCESS':
        result = []
        for field in dict_data['images'][0]['fields']:
            result.append({
                # 'name': field['name'],
                # 'inferText': field['inferText']
                field['name']: field['inferText']
            })
    result_dict = {
        'template_name': dict_data['images'][0]['matchedTemplate']['name'],
        'results': result
    }
    from pprint import pprint
    pprint(result_dict)
