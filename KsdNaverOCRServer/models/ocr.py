from sqlalchemy import Column, DateTime, Integer, String

from KsdNaverOCRServer.database import Base
from KsdNaverOCRServer.models.models_function import get_now_time


class OcrResult(Base):
    __tablename__ = "ocr_result"
    id = Column(Integer, primary_key=True, index=True)
    result_file_name = Column(String)
    category = Column(String)
    created_time = Column(DateTime, default=get_now_time())

    user_id = Column(String, nullable=False)
