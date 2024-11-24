import logging

import logfire
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.category.schemas import OCRShowV3, RequestOCRV3
from app.database.core import get_db
from app.naver_clova_ocr.schemas import ClovaOCRResponseV3
from app.ocr.services import find_best_matching_category, process_category_ocr, process_general_ocr

ocr_router_v4 = APIRouter(prefix="/v4")

logger = logging.getLogger(__name__)


@ocr_router_v4.post("/ocr", status_code=status.HTTP_201_CREATED, response_model=OCRShowV3)
async def process_image_view(request_body: RequestOCRV3, db_session: Session = Depends(get_db)):
    """
    ---

    # Request Body
        {
          "image_url": "string", # public 접근 가능한 image url
          "file_name_extension": "string" # image url 의 파일 확장자
        }

    ---

    # Response Body

        {
          "category": "string", # 아래 작성되어있는 분류 항목의 카테고리
          "domain_name": "string", # 아래 작성되어있는 분류 항목 domain_name
          "result": json # Naver Clova OCR 결과 - 참고 문헌 1 참고
        }

    ---

    # 분류 항목

        [
          {
            "domain_description": "0 처방전",
            "domain_name": "Prescription",
            "category": "PR",
          },
          {
            "domain_description": "1 의학적검진",
            "domain_name": "Medical Examination",
            "category": "ME",
          },
          {
            "domain_description": "2 인지및지능검사",
            "domain_name": "Perception and Intelligence Test",
            "category": "PI",
          },
          {
            "domain_description": "3 사회성 및 자폐검사",
            "domain_name": "Sociality & Autism Test",
            "category": "SA",
          },
          {
            "domain_description": "4 언어평가",
            "domain_name": "Language Tests",
            "category": "LR",
          },
          {
            "domain_description": "5 주의력 및 신경인지검사",
            "domain_name": "Attention and Neurocognitive Function Test",
            "category": "AN",
          },
          {
            "domain_description": "6 기질 성격 정서검사",
            "domain_name": "Temperament and Character And Emotion Test",
            "category": "TC",
          },
          {
            "domain_description": "7 학습검사",
            "domain_name": "Learning Test",
            "category": "LT",
          },
          {
            "domain_description": "8 발달 평가 결과",
            "domain_name": "Infant Health Checkup",
            "category": "IH",
          }
        ]

    ---
    # 참고 문헌

    ## 1. Naver CLOVA OCR Custom API
    - ### [https://api.ncloud-docs.com/docs/ai-application-service-ocr-ocr#v2-응답-바디](https://api.ncloud-docs.com/docs/ai-application-service-ocr-ocr#v2-응답-바디)

    """
    general_result = await process_general_ocr(db_session, request_body.image_url, request_body.file_name_extension)

    if general_result is None:
        return "general ocr result is None -> Error"

    categories = find_best_matching_category(db_session, general_result)
    if categories is []:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"msg": "category search fail", "general_ocr_result": general_result.model_dump()},
        )
    logfire.info(f"target_categories = {[category.name for category in categories]}")

    category_result, category = await process_category_ocr(
        image_url=request_body.image_url, image_format=request_body.file_name_extension, categories=categories
    )

    return OCRShowV3(category=category.name, domain_name=category.description, result=category_result)


@ocr_router_v4.post("/general-ocr", status_code=status.HTTP_201_CREATED, response_model=ClovaOCRResponseV3 | str)
async def process_genaral_image_view(request_body: RequestOCRV3, db_session: Session = Depends(get_db)):
    """이미지 URL을 받아 General OCR 처리를 합니다. - Debug 용"""
    general_result = await process_general_ocr(db_session, request_body.image_url, request_body.file_name_extension)

    if general_result is None:
        return "general ocr result is None -> Error"

    return general_result
