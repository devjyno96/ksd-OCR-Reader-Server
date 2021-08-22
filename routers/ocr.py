import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, status, File, UploadFile, Form

from sqlalchemy.orm import Session

from repository import ocr as ocr_repository

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
    return ocr_repository.ocr_request(request)


# User Id를 추가한 요청
@router.post('/user', status_code=status.HTTP_201_CREATED)
def ocr_request_by_user(request: ocr_schemas.RequestOCRByUser):
    '''
    OCR 분석 요청
    User_Id를 추가해서 요청
    '''
    return ocr_repository.ocr_request_by_user(request)


# 결과 받기
@router.get('/result', status_code=status.HTTP_200_OK)
def get_ocr_result_bu_OCR_ID(ocr_id: int):
    """
    OCR 분석 결과 중 해당 id의 결과 불러오기
    """
    return get_ocr_result_bu_OCR_ID(ocr_id)


@router.get('/result/user', status_code=status.HTTP_200_OK)
def get_ocr_result_by_user(request: ocr_schemas.RequestOCR):
    """
    OCR 분석 결과 중 해당 user id의 모든 결과 불러오기
    """
    pass


@router.get('/all', status_code=status.HTTP_200_OK)
def get_ocr_result_all(request: ocr_schemas.RequestOCR):
    """
    OCR 분석 결과 전체 불러오기
    """
    pass


@router.delete('/result', status_code=status.HTTP_204_NO_CONTENT)
def delete_ocr_result(ocr_id: int):
    """
    OCR 분석 결과 삭제
    """
    pass
