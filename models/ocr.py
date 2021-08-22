from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship

from .models_function import get_now_time
from database import Base


class OcrResult(Base):
    __tablename__ = 'ocr_result'
    id = Column(Integer, primary_key=True, index=True)
    result_file_name = Column(String)
    created_time = Column(DateTime, default=get_now_time())

    # User : Ocr_result = 1 : N
    user_id = Column(Integer, ForeignKey('users.id'))
    ocr_results = relationship("User", back_populates="ocr_results", foreign_keys=[user_id])
