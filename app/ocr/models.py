from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.naver_clova_ocr.models import NaverClovaOCR

if TYPE_CHECKING:
    from app.category.models import Category


class GeneralOCR(NaverClovaOCR):
    __tablename__ = "general_ocrs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


class CategoryOCR(NaverClovaOCR):
    __tablename__ = "category_ocrs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    category: Mapped["Category"] = relationship("Category", back_populates="category_ocr_configs")
