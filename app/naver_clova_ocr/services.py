import httpx


async def call_ocr_api(api_url: str, api_key: str, image_url: str):
    """네이버 OCR API를 호출하여 이미지를 처리합니다."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            api_url,
            headers={"X-OCR-SECRET": api_key},
            json={"image_url": image_url},
        )
    return response.json()
