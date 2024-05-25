from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.core import Base

if TYPE_CHECKING:
    from app.ocr.models import CategoryOCR


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="Primary key of the category")
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, comment="Name of the category")
    keywords: Mapped[list["CategoryKeyword"]] = relationship("CategoryKeyword", back_populates="category")
    category_ocr_configs: Mapped[list["CategoryOCR"]] = relationship("CategoryOCR", back_populates="category")


class CategoryKeyword(Base):
    __tablename__ = "category_keywords"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="Primary key of the category keyword")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'), nullable=False, comment="Foreign key referencing the category")
    keyword: Mapped[str] = mapped_column(String, nullable=False, comment="Keyword associated with the category")
    category: Mapped["Category"] = relationship("Category", back_populates="keywords")