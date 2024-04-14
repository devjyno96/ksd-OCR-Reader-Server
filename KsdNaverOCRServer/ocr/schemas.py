from datetime import datetime
from typing import Dict

from pydantic import BaseModel

from KsdNaverOCRServer.enums import CategoryEnum


class RequestOCRV3(BaseModel):
    image_url: str
    file_name_extension: str
    category: CategoryEnum


class OCRShowV3(BaseModel):
    ocr_id: int
    user_id: str
    category: str
    domain_name: str
    created_time: datetime
    ocr_result: Dict
