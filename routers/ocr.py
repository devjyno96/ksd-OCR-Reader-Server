import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, status, File, UploadFile, Form

from sqlalchemy.orm import Session

from repository import ocr as oct_repository

from schemas import ocr as ocr_schemas

# from .. import database


router = APIRouter(
    prefix='/ocr',
    tags=['Ocr']
)


# get_db = database.get_db

@router.post('/', status_code=status.HTTP_201_CREATED)
def ocr_request(request: ocr_schemas.RequestOCR):
    '''
    OCR 분석 요청
    '''
    return oct_repository.ocr_request(request)
