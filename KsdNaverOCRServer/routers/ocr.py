import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, status, File, UploadFile, Form

from sqlalchemy.orm import Session

from KsdNaverOCRServer.repository import ocr as ocr_repository

from KsdNaverOCRServer.schemas import ocr as ocr_schemas

import KsdNaverOCRServer.database

router = APIRouter(
    prefix='/ocr',
    tags=['Ocr']
)

get_db = KsdNaverOCRServer.database.get_db


@router.post('/', status_code=status.HTTP_201_CREATED)
def ocr_request(request: ocr_schemas.RequestOCR):
    '''
    OCR 분석 요청
    '''
    return ocr_repository.ocr_request(request)


# User Id를 추가한 요청
@router.post('/user', status_code=status.HTTP_201_CREATED)
def ocr_request_by_user(request: ocr_schemas.RequestOCRByUser, db: Session = Depends(get_db)):
    '''
    OCR 분석 요청
    User_Id를 추가해서 요청
    '''
    return ocr_repository.ocr_request_by_user(request, db)


# 결과 받기
@router.get('/result', status_code=status.HTTP_200_OK)
def get_ocr_result_by_OCR_ID(ocr_id: int, db: Session = Depends(get_db)):
    """
    OCR 분석 결과 중 해당 id의 결과 불러오기
    """
    return ocr_repository.get_ocr_result_by_OCR_ID(ocr_id, db)


@router.get('/result/user', status_code=status.HTTP_200_OK)
def get_ocr_result_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    OCR 분석 결과 중 해당 user id의 모든 결과 불러오기
    """
    return ocr_repository.get_ocr_result_by_user(user_id, db)


@router.get('/all', status_code=status.HTTP_200_OK)
def get_ocr_result_all(db: Session = Depends(get_db)):
    """
    OCR 분석 결과 전체 불러오기
    """
    return ocr_repository.get_ocr_result_all(db)


@router.delete('/result', status_code=status.HTTP_204_NO_CONTENT)
def delete_ocr_result(ocr_id: int, db: Session = Depends(get_db)):
    """
    OCR 분석 결과 삭제
    """
    return ocr_repository.delete_ocr_result(ocr_id, db)
