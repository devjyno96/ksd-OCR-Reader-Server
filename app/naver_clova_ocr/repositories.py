import threading
import time

import httpx
import requests
from fastapi import status

from app.naver_clova_ocr.models import NaverClovaOCR
from app.naver_clova_ocr.schemas import ClovaOCRResponseV3
from KsdNaverOCRServer.config import GENERAL_OCR_DOMAIN_KEY, NAVER_OCR_DOMAIN_KEY_LIST
from KsdNaverOCRServer.naver_clova.schemas import ClovaOCRRequestV3, ImageRequestV3


class NaverOCRRepository:
    async def request_ocr_to_naver_clova_api(
        self, image_url: str, image_format: str, naver_clova_ocr: NaverClovaOCR
    ) -> ClovaOCRResponseV3 | None:
        """네이버 OCR API를 호출하여 이미지를 처리합니다."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                naver_clova_ocr.ocr_api_url,
                headers={"X-OCR-SECRET": naver_clova_ocr.ocr_api_key},
                json={
                    "images": [{"format": image_format, "name": "image", "url": image_url}],
                    "requestId": "ocr-request",
                    "version": "V2",
                    "timestamp": int(round(time.time() * 1000)),
                },
            )

        if response.status_code != status.HTTP_200_OK:
            return None

        return ClovaOCRResponseV3.model_validate(response.json())


naver_ocr_repository = NaverOCRRepository()


def get_ocr_key_by_category(category: str):
    if category == GENERAL_OCR_DOMAIN_KEY["category"]:
        return GENERAL_OCR_DOMAIN_KEY
    if category == "CI":
        return NAVER_OCR_DOMAIN_KEY_LIST[1]["sub_domain_list"][1]
    for ocr_key in NAVER_OCR_DOMAIN_KEY_LIST:
        if ocr_key["category"] == category:
            return ocr_key


def ocr_request_by_image_url(image_url: str, file_name_extension: str, ocr_key) -> ClovaOCRResponseV3:
    request_body = ClovaOCRRequestV3(
        images=[
            ImageRequestV3(
                format=file_name_extension,
                name="image",
                url=image_url,
            )
        ],
        requestId="ocr-request",
        version="V2",
    )
    payload = request_body.model_dump_json()
    headers = {"X-OCR-SECRET": ocr_key["secret_key"], "Content-Type": "application/json"}

    response = requests.post(url=ocr_key["APIGW_Invoke_url"], headers=headers, data=payload).json()
    result = ClovaOCRResponseV3.model_validate(response)
    return result


def multithread_ocr_request_by_image_url(
    image_url: str, file_name_extension: str, ocr_keys: list[dict]
) -> list[ClovaOCRResponseV3]:
    threads = []
    results = []

    def thread_ocr_request(image_url: str, file_name_extension: str, ocr_key, results: list):
        result = ocr_request_by_image_url(image_url, file_name_extension, ocr_key)
        results.append(result)

    for ocr_key in ocr_keys:
        thread = threading.Thread(target=thread_ocr_request, args=(image_url, file_name_extension, ocr_key, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results
