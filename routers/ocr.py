import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, status, File, UploadFile, Form

from sqlalchemy.orm import Session

from repository import ocr as oct_repository

# from .. import database


router = APIRouter(
    prefix='/ocr',
    tags=['Ocr']
)

# get_db = database.get_db

@router.post('/', status_code=status.HTTP_201_CREATED)
def ocr_create(s3_url: str, ocr_type: str):
    '''
    OCr 분석 요청
    '''
    return oct_repository.ocr_create(s3_url, ocr_type)
