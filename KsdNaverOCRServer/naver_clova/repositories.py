import json
import time

import requests

from KsdNaverOCRServer.config import GENERAL_OCR_DOMAIN_KEY, NAVER_OCR_DOMAIN_KEY_LIST
from KsdNaverOCRServer.naver_clova.schemas import OCRResponseV2


def get_ocr_key_by_category(category: str):
    if category == GENERAL_OCR_DOMAIN_KEY["category"]:
        return GENERAL_OCR_DOMAIN_KEY
    if category == "CI":
        return NAVER_OCR_DOMAIN_KEY_LIST[1]["sub_domain_list"][1]
    for ocr_key in NAVER_OCR_DOMAIN_KEY_LIST:
        if ocr_key["category"] == category:
            return ocr_key


def ocr_request_by_url(image_url: str, file_name_extension: str, category, ocr_key=None) -> OCRResponseV2:
    if ocr_key is None:
        ocr_key = get_ocr_key_by_category(category)
    request_json = {
        "images": [{"format": file_name_extension, "name": "image", "url": image_url}],
        "requestId": "ocr-request",
        "version": "V2",
        "timestamp": int(round(time.time() * 1000)),
    }

    payload = json.dumps(request_json).encode("UTF-8")
    headers = {"X-OCR-SECRET": ocr_key["secret_key"], "Content-Type": "application/json"}

    response = requests.post(url=ocr_key["APIGW_Invoke_url"], headers=headers, data=payload).json()
    result = OCRResponseV2.model_validate(response)
    return result
