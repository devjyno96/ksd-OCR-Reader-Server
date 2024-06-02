from app.ocr.models import CategoryOCR, GeneralOCR
from app.ocr.schemas import CategoryOCRCreate, CategoryOCRUpdate, GeneralOCRCreate, GeneralOCRUpdate
from app.repositories import BaseRepository


class GeneralOCRRepository(BaseRepository[GeneralOCR, GeneralOCRCreate, GeneralOCRUpdate]): ...


class CategoryOCRRepository(BaseRepository[CategoryOCR, CategoryOCRCreate, CategoryOCRUpdate]): ...


general_ocr_repository = GeneralOCRRepository(GeneralOCR)
category_ocr_repository = CategoryOCRRepository([CategoryOCR, CategoryOCRCreate, CategoryOCRUpdate])
