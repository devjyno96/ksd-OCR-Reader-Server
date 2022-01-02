import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, status, File, UploadFile, Form

from sqlalchemy.orm import Session

from KsdNaverOCRServer.repository import ocr as ocr_repository

from KsdNaverOCRServer.schemas import ocr as ocr_schemas

import KsdNaverOCRServer.database

from KsdNaverOCRServer.enums import CategoryEnum

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


@router.post('/v2', status_code=status.HTTP_201_CREATED)
def ocr_request_v2(category: CategoryEnum = Form(...), image_file: UploadFile = File(...), db: Session = Depends(get_db)):
    '''
    OCR 분석 요청
    해당 category에 맞게 string으로 넘겨주시면 됩니다.
    TOTAL의 경우 아래 카테고리 중 해당하는 카테고리를 찾아서 반환해 줍니다.

        [
          {
            "domain_description": "1. 발달력 및 신체성장",
            "domain_name": "Development & Physical growth",
            "category": "DP"
          },
          {
            "domain_description": "2. 혈액 검사",
            "domain_name": "Medical checkup",
            "category": "MC"
          },
          {
            "domain_description": "3. 발달 및 지능검사",
            "domain_name": "Development & Intelligence test",
            "category": "DI"
          },
          {
            "domain_description": "4. 사회성 및 자폐검사",
            "domain_name": "Sociality & Autism tests",
            "category": "SA"
          },
          {
            "domain_description": "5. 언어 및 신경인지검사",
            "domain_name": "Language test",
            "category": "LR"
          },
          {
            "domain_description": "6. 기질 및 성격검사",
            "domain_name": "Temperament & Personality & Emotional state",
            "category": "TC"
          },
          {
            "domain_description": "7. 주의력 및 기질 및 학습검사",
            "domain_name": "Attention & Neurocognition & Learning tests",
            "category": "AL"
          },
          {
            "domain_description": "8. 전체 검사",
            "domain_name": "Attention & Neurocognition & Learning tests",
            "category": "TOTAL"
          }
        ]
    '''
    return ocr_repository.ocr_request_v2(category, image_file, db)


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


@router.delete('/result/user', status_code=status.HTTP_204_NO_CONTENT)
def get_ocr_result_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    OCR 분석 결과 중 해당 user id의 모든 결과 삭제하기
    """
    return ocr_repository.delete_ocr_result_by_user(user_id, db)


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
