from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.core import Base

if TYPE_CHECKING:
    from app.ocr.models import CategoryOCR


class Category(Base):
    __tablename__ = "categories"

    def __str__(self):
        return f"id={self.id}, name={self.name}, description={self.description}"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="Primary key of the category")
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, comment="Name of the category")
    description: Mapped[str] = mapped_column(String, nullable=False, unique=True, comment="Description of the category")
    keywords: Mapped[list["CategoryKeyword"]] = relationship("CategoryKeyword", back_populates="category")
    category_ocr_configs: Mapped[list["CategoryOCR"]] = relationship("CategoryOCR", back_populates="category")

    @property
    def category_keywords(self) -> list[str]:
        return [category_keyword.keyword for category_keyword in self.keywords]


class CategoryKeyword(Base):
    __tablename__ = "category_keywords"

    def __str__(self):
        return f"id={self.id}, category_id={self.category_id}, keyword={self.keyword}"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, comment="Primary key of the category keyword"
    )
    keyword: Mapped[str] = mapped_column(String, nullable=False, comment="Keyword associated with the category")
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.id"), nullable=False, comment="Foreign key referencing the category"
    )
    category: Mapped["Category"] = relationship("Category", back_populates="keywords")
