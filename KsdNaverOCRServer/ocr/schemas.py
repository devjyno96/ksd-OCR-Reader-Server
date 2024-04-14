from pydantic import BaseModel

from KsdNaverOCRServer.enums import CategoryEnum


class RequestOCRV3(BaseModel):
    image_url: str
    file_name_extension: str
    category: CategoryEnum


class OCRShowV3(BaseModel):
    category: str
    domain_name: str
    ocr_result: dict
