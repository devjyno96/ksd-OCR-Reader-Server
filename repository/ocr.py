import sqlalchemy
from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session

# from ..models import test as test_models

from schemas import ocr as ocr_schemas

import requests
import time
import json, os

from resources.naver_ocr_domain_key import NAVER_OCR_DOMAIN_KEY as ocr_keys


RESULT_FILE = os.getcwd() + "/result/"

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


# Terminal Test용
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


# User Id를 추가한 요청
def ocr_request_by_user(request: ocr_schemas.RequestOCRByUser):
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

    # save result by user
    file_name = f"""{request.user_id}-{json.loads(response.text)['timestamp']}.json"""
    with open(RESULT_FILE + file_name, "w") as json_file:
        json.dump(json.loads(response.text), json_file)

    return json.loads(response.text)


# 결과 받기
def get_ocr_result_bu_OCR_id(ocr_id : int):
    pass


def get_ocr_result_by_user(request: ocr_schemas.RequestOCR):
    """
    OCR 분석 결과 받기
    """
    pass


def get_ocr_result_all(request: ocr_schemas.RequestOCR):
    """
    OCR 분석 결과 받기
    """
    pass


def delete_ocr_result(request: ocr_schemas.RequestOCR):
    """
    OCR 분석 결과 받기
    """
    pass
