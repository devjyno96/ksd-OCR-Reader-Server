import sqlalchemy
from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session

# from ..models import test as test_models

# from ..schemas import admin_dashboard as admin_dashboard_schemas


def ocr_create(s3_url: str, ocr_type: str):
    pass