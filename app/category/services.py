from KsdNaverOCRServer.config import NAVER_OCR_DOMAIN_KEY_LIST
from KsdNaverOCRServer.naver_clova.repositories import (
    get_ocr_key_by_category,
    multithread_ocr_request_by_image_url,
    ocr_request_by_image_url,
)
from KsdNaverOCRServer.naver_clova.schemas import ClovaOCRResponseV3
from KsdNaverOCRServer.ocr.schemas import OCRShowV3
from KsdNaverOCRServer.ocr.typed import MedicalExaminationConfig


def find_ocr_domains(image_url: str, file_name_extension: str) -> list[MedicalExaminationConfig]:
    general_ocr_key = get_ocr_key_by_category("GENERAL")
    general_ocr_response = ocr_request_by_image_url(
        image_url=image_url,
        file_name_extension=file_name_extension,
        ocr_key=general_ocr_key,
    )
    ocr_key = find_template_in_OCR_response(general_ocr_response)
    return NAVER_OCR_DOMAIN_KEY_LIST if ocr_key is None else [ocr_key]


def find_template_in_OCR_response(ocr_response: ClovaOCRResponseV3) -> MedicalExaminationConfig | None:
    """
    general ocr 속에 domain key word를 가장 많이 포함한 domain을 찾는다
    """
    general_ocr_result = None
    if ocr_response.is_successed:
        general_ocr_result = [x.inferText for x in ocr_response.images[0].fields]

    if general_ocr_result is None:
        return None

    total_str = ""

    for word in general_ocr_result:
        total_str += word

    return_domain = NAVER_OCR_DOMAIN_KEY_LIST[0]
    max_count = 0
    for domain in NAVER_OCR_DOMAIN_KEY_LIST:
        count = 0
        for word in domain["domain_keyword_list"]:
            if word in total_str:
                count += 1
        if count > max_count:
            max_count = count
            return_domain = domain

    return return_domain


def ocr_requests_by_image_url(image_url: str, file_name_extension: str, ocr_keys=list[MedicalExaminationConfig]):
    result_dict = []
    for ocr_key in ocr_keys:
        request_sub_domain = [ocr_key]
        if "sub_domain_list" in ocr_key:
            request_sub_domain = ocr_key["sub_domain_list"]
        responses = multithread_ocr_request_by_image_url(
            image_url=image_url, file_name_extension=file_name_extension, ocr_keys=request_sub_domain
        )
        for response in responses:
            if response.is_successed:
                # 도메인이 2인 경우 반환은 서브 도메인이 아닌 일반 도메인으로 반환
                result_dict.append({"domain_ocr_key": ocr_key, "response": response})
    return result_dict


def select_best_ocr_result(results: list[dict]) -> dict:
    def get_blank_count(response_dict):
        return sum(1 for f in response_dict["response"].images[0].fields if len(f.inferText) == 0)

    best_result = min(results, key=get_blank_count)
    return best_result


def handle_ocr_results(result_dict: list[dict]) -> OCRShowV3:
    result = select_best_ocr_result(result_dict)

    response: ClovaOCRResponseV3 = result["response"]
    ocr_key = result["domain_ocr_key"]

    return OCRShowV3(
        category=ocr_key["category"],
        domain_name=ocr_key["domain_name"],
        result=response,
    )
