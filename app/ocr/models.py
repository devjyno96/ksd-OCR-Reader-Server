from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.naver_clova_ocr.models import NaverClovaOCR

if TYPE_CHECKING:
    from app.category.models import Category


class GeneralOCR(NaverClovaOCR):
    __tablename__ = "general_ocrs"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, comment="Primary key of the general OCR settings"
    )


class CategoryOCR(NaverClovaOCR):
    __tablename__ = "category_ocrs"

    def __str__(self):
        return f"id={self.id}, category_id={self.category_id}, category_name={self.category.name}"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, comment="Primary key of the category OCR settings"
    )

    # relation
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.id"), nullable=False, comment="Foreign key referencing the category"
    )
    category: Mapped["Category"] = relationship("Category", back_populates="category_ocr_configs")
