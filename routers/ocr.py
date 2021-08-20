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

# User Id를 추가한 요청
@router.post('/', status_code=status.HTTP_201_CREATED)
def ocr_request_by_user(request: ocr_schemas.RequestOCRByUser):
    '''
    OCR 분석 요청
    User_Id를 추가해서 요청
    '''
    return oct_repository.ocr_request(request)


# 결과 받기
@router.get('/result', status_code=status.HTTP_200_OK)
def get_ocr_result(request: ocr_schemas.RequestOCR):
    """
    OCR 분석 결과 받기
    """
    pass


@router.get('/result/user', status_code=status.HTTP_200_OK)
def get_ocr_result_by_user(request: ocr_schemas.RequestOCR):
    """
    OCR 분석 결과 받기
    """
    pass


@router.get('/all', status_code=status.HTTP_200_OK)
def get_ocr_result_all(request: ocr_schemas.RequestOCR):
    """
    OCR 분석 결과 받기
    """
    pass


@router.delete('/result', status_code=status.HTTP_204_NO_CONTENT)
def delete_ocr_result(request: ocr_schemas.RequestOCR):
    """
    OCR 분석 결과 받기
    """
    pass
