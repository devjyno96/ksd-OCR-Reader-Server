from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.core import Base


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    keywords: Mapped[list["CategoryKeyword"]] = relationship("CategoryKeyword", back_populates="category")
    category_ocr_configs: Mapped[list["CategoryOCR"]] = relationship("CategoryOCR", back_populates="category")


class CategoryKeyword(Base):
    __tablename__ = "category_keywords"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    keyword: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped["Category"] = relationship("Category", back_populates="keywords")


class CategoryOCR(Base):
    __tablename__ = "category_ocrs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    ocr_api_url: Mapped[str] = mapped_column(String, nullable=False)
    ocr_api_key: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped["Category"] = relationship("Category", back_populates="category_ocr_configs")
