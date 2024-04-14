from datetime import datetime
from typing import Dict

from pydantic import BaseModel

from KsdNaverOCRServer.enums import CategoryEnum


class RequestOCR(BaseModel):
    image_url: str
    file_name_extension: str
    category: CategoryEnum


class RequestOCRByUser(RequestOCR):
    user_id: str


class ShowRequestOCR(BaseModel):
    ocr_id: int
    user_id: str
    category: str
    domain_name: str
    created_time: datetime
    ocr_result: Dict


class OCRShowV3(BaseModel):
    category: str
    domain_name: str
    created_time: datetime
    ocr_result: Dict
