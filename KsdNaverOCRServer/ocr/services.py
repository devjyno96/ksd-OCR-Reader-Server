import json
import time

import requests

from KsdNaverOCRServer.config import GENERAL_OCR_DOMAIN_KEY
from KsdNaverOCRServer.config import NAVER_OCR_DOMAIN_KEY_LIST as ocr_keys
from KsdNaverOCRServer.ocr.schemas import OCRShowV3
from KsdNaverOCRServer.ocr.typed import MedicalExaminationConfig


def find_template(general_ocr_result):
    """
    general ocr 속에 domain key word를 가장 많이 포함한 domain을 찾는다
    """
    total_str = ""

    for word in general_ocr_result:
        total_str += word

    return_domain = ocr_keys[0]
    max_count = 0
    for domain in ocr_keys:
        count = 0
        for word in domain["domain_keyword_list"]:
            if word in total_str:
                count += 1
        # Todo 판단 알고리즘 변경
        # 지금은 카운드 갯수로만 비교 -> 전체 퍼센트로 변경
        if count > max_count:
            # if count / len(domain['domain_keyword_list']) > max_count_percent:
            max_count = count
            # max_count_percent = count / len(domain['domain_keyword_list'])
            return_domain = domain

    return return_domain


def request_general_ocr(
    image_url: str,
    file_name_extension: str,
):
    general_ocr_result = None
    response = ocr_request_by_url(image_url=image_url, file_name_extension=file_name_extension, category="GENERAL")
    if "images" in response:
        if response["images"][0]["inferResult"] == "SUCCESS":
            general_ocr_result = [x["inferText"] for x in response["images"][0]["fields"]]
    return general_ocr_result


def get_domain_by_image_url(
    image_url: str,
    file_name_extension: str,
):
    general_ocr_result = request_general_ocr(image_url=image_url, file_name_extension=file_name_extension)
    if general_ocr_result is None:
        return None
    return find_template(general_ocr_result)


def get_ocr_key_by_category(category: str):
    if category == GENERAL_OCR_DOMAIN_KEY["category"]:
        return GENERAL_OCR_DOMAIN_KEY
    if category == "CI":
        return ocr_keys[1]["sub_domain_list"][1]
    for ocr_key in ocr_keys:
        if ocr_key["category"] == category:
            return ocr_key


def ocr_request_by_url(image_url: str, file_name_extension: str, category, ocr_key=None):
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
    return response


def ocr_requests_by_image_url(image_url: str, file_name_extension: str, ocr_keys=list[MedicalExaminationConfig]):
    result_dict = []
    for ocr_key in ocr_keys:
        request_sub_domain = [ocr_key]
        if "sub_domain_list" in ocr_key:
            request_sub_domain = ocr_key["sub_domain_list"]

        for sub_domain_key in request_sub_domain:
            response = ocr_request_by_url(
                image_url=image_url,
                file_name_extension=file_name_extension,
                category=sub_domain_key["category"],
                ocr_key=sub_domain_key,
            )

            if "images" in response:
                if response["images"][0]["inferResult"] == "SUCCESS":
                    # 도메인이 2인 경우 반환은 서브 도메인이 아닌 일반 도메인으로 반환
                    result_dict.append({"domain_ocr_key": ocr_key, "response": response})
    return result_dict


def ocr_result_filter(response):
    if response["images"][0]["inferResult"] == "SUCCESS":
        result = {}
        for field in response["images"][0]["fields"]:
            result[field["name"]] = field["inferText"]

        result_dict = {"template_name": response["images"][0]["matchedTemplate"]["name"], "results": result}
        return result_dict
    else:
        return None


def find_ocr_domains(image_url: str, file_name_extension: str) -> list[MedicalExaminationConfig]:
    ocr_key = get_domain_by_image_url(
        image_url=image_url,
        file_name_extension=file_name_extension,
    )

    return ocr_keys if ocr_key is None else [ocr_key]


def select_best_result(results: list[dict]) -> dict:
    def get_blank_count(response_dict):
        return sum(1 for f in response_dict["response"]["images"][0]["fields"] if len(f["inferText"]) == 0)

    best_result = min(results, key=get_blank_count)
    return best_result


def process_ocr_result(response: dict, ocr_key: dict) -> OCRShowV3:
    filtered_result = ocr_result_filter(response)

    return OCRShowV3(
        category=ocr_key["category"],
        domain_name=ocr_key["domain_name"],
        ocr_result=filtered_result,
    )


def handle_ocr_results(result_dict: list[dict]) -> OCRShowV3:
    result = select_best_result(result_dict)

    response = result["response"]
    ocr_key = result["domain_ocr_key"]

    return process_ocr_result(response, ocr_key)
