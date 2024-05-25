from pydantic import BaseModel


class OCRRequest(BaseModel):
    image_url: str


class OCRResponse(BaseModel):
    general_result: dict
    category_result: list
