from pydantic import BaseModel, Field

from app.naver_clova_ocr.schemas import ClovaOCRResponseV3


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


class CategoryBase(BaseModel):
    name: str
    description: str


class CategoryCreate(CategoryBase):
    pass


class CategoryShowV1(CategoryBase):
    id: int


class CategoryUpdate(CategoryBase):
    id: int


class CategoryKeywordBase(BaseModel):
    category_id: int
    keyword: str


class CategoryKeywordCreate(CategoryKeywordBase):
    pass


class CategoryKeywordUpdate(CategoryKeywordBase):
    id: int


class CategoryKeywordShowV1(CategoryKeywordBase):
    id: int
