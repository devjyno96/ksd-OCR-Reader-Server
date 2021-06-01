import datetime
from pytz import timezone
import enum

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

# from ..database import Base

# from .models_function import get_now_time

#
# class AuditProgram(Base):
#     __tablename__ = 'audit_programs'
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     due_date = Column(DateTime)
#     possible_results = Column(String)
#     from_date = Column(DateTime)
#     to_date = Column(DateTime)
#     parent_id = Column(Integer)
#
#     controls = relationship("Control", back_populates="audit_program", passive_deletes=True)
#
#     test_types = relationship("TestType", back_populates="audit_program", passive_deletes=True)
#
#     admin_user = relationship("AdminUser", back_populates="audit_program", passive_deletes=True)