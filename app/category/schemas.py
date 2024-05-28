from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field

from KsdNaverOCRServer.enums import CategoryEnum
from KsdNaverOCRServer.naver_clova.schemas import ClovaOCRResponseV3


class RequestOCRV3(BaseModel):
    image_url: str = Field(..., description="URL은 이미지를 가져 올 수 있는 공개 URL이어야 함")
    file_name_extension: str = Field(
        ...,
        description="""이미지 포맷 설정, “jpg”, “jpeg”, “png”, "pdf","tiff" 이미지 포맷 지원. General OCR: 최대 10페이지의 pdf 인식 지원, Template OCR: 최대 5페이지의 pdf/tiff 인식 지원 """,
    )


class OCRShowV3(BaseModel):
    category: str = Field(..., description="category")
    domain_name: str = Field(..., description="domain_name")
    result: ClovaOCRResponseV3 = Field(..., description="Naver Clova Custom API V2 응답 바디 결과")


class RequestOCR(BaseModel):
    image_url: str
    file_name_extension: str
    category: CategoryEnum


class RequestOCRByUser(RequestOCR):
    user_id: str


class ShowRequestOCR(BaseModel):
    ocr_id: int
    user_id: int
    category: str
    domain_name: str
    created_time: datetime
    ocr_result: Dict


class CategoryBase(BaseModel):
    name: str
    description: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    id: int


class CategoryKeywordBase(BaseModel):
    category_id: int
    keyword: str


class CategoryKeywordCreate(CategoryKeywordBase):
    pass


class CategoryKeywordUpdate(CategoryKeywordBase):
    id: int
