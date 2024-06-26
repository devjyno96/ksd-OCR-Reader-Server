from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.core import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_admin = Column(Boolean)

    # One To One
    profile = relationship("Profile", uselist=False, back_populates="user")
    refresh_token = relationship("RefreshToken", uselist=False, back_populates="user")

    # User-AdminUser : 1 to n
    admin_user = relationship("AdminUser", back_populates="user", passive_deletes=True)

    # User : OCR_Result = 1 to n
    # ocr_results = relationship("OcrResult", back_populates="ocr_results")


class Profile(Base):
    __tablename__ = "profiles"

    # id = Column(Integer, primary_key=True, index=True)
    # User-Profile : One To One
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship("User", back_populates="profile")

    email = Column(String, unique=True)


class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="admin_user")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    user = relationship("User", back_populates="refresh_token")

    token = Column(String)
