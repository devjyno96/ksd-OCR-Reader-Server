from pydantic import BaseModel


class OCRRequest(BaseModel):
    image_url: str


class OCRResponse(BaseModel):
    general_result: dict
    category_result: list


class GeneralOCRBase(BaseModel):
    ocr_api_url: str
    ocr_api_key: str


class GeneralOCRCreate(GeneralOCRBase):
    pass


class GeneralOCRUpdate(GeneralOCRBase):
    id: int


class CategoryOCRBase(BaseModel):
    id: int
    ocr_api_url: str
    ocr_api_key: str
    category_id: int


class CategoryOCRCreate(CategoryOCRBase):
    pass


class CategoryOCRUpdate(CategoryOCRBase):
    id: int
