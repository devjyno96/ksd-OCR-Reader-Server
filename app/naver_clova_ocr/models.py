from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.core import Base


class NaverClovaOCR(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="Primary key of the OCR settings")
    ocr_api_url: Mapped[str] = mapped_column(String, nullable=False, comment="URL of the OCR API")
    ocr_api_key: Mapped[str] = mapped_column(String, nullable=False, comment="API key for the OCR service")
