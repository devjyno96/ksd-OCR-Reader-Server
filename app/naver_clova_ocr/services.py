import time

import httpx
from fastapi import status

from app.naver_clova_ocr.schemas import ClovaOCRResponseV3


async def call_naver_ocr_api(
    api_url: str, api_key: str, image_url: str, image_format: str
) -> ClovaOCRResponseV3 | None:
    """네이버 OCR API를 호출하여 이미지를 처리합니다."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            api_url,
            headers={"X-OCR-SECRET": api_key},
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
