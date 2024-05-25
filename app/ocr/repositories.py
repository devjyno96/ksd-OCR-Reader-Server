from sqlalchemy.orm import Session

from app.ocr.models import CategoryOCR, GeneralOCR


class OCRRepository:
    def get_general_ocr(self, db: Session):
        """일반 OCR 설정을 가져옵니다."""
        return db.query(GeneralOCR).first()

    def get_category_ocr(self, db: Session, category_id: int):
        """특정 카테고리의 OCR 설정을 가져옵니다."""
        return db.query(CategoryOCR).filter(CategoryOCR.category_id == category_id).all()
