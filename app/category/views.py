from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.category.repositories import category_repository
from app.category.schemas import CategoryKeywordCreate, CategoryKeywordShowV1, CategoryShowV1, OCRShowV3, RequestOCRV3
from app.category.services import (
    bulk_udpate_catetory_keywords,
    find_ocr_domains,
    handle_ocr_results,
    ocr_requests_by_image_url,
)
from app.database.core import get_db

ocr_v3_router = APIRouter(prefix="/v3/ocr", tags=["OCR"])
catetory_v1_debug_router = APIRouter(prefix="/v1/debug/catetory", tags=["Category"])


@ocr_v3_router.post("", status_code=status.HTTP_201_CREATED, response_model=OCRShowV3)
def ocr_request_v3_by_url(request_body: RequestOCRV3, db: Session = Depends(get_db)):
    """
    # 삭제 될 API 입니다

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
          }
        ]

    ---
    # 참고 문헌

    ## 1. Naver CLOVA OCR Custom API
    - ### [https://api.ncloud-docs.com/docs/ai-application-service-ocr-ocr#v2-응답-바디](https://api.ncloud-docs.com/docs/ai-application-service-ocr-ocr#v2-응답-바디)

    """
    ocr_keys = find_ocr_domains(image_url=request_body.image_url, file_name_extension=request_body.file_name_extension)
    results = ocr_requests_by_image_url(
        image_url=request_body.image_url, file_name_extension=request_body.file_name_extension, ocr_keys=ocr_keys
    )
    result = handle_ocr_results(results)
    return result


@catetory_v1_debug_router.get("/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryShowV1)
def get_catetory_v1_debug(category_id: int, db: Session = Depends(get_db)):
    """
    # Debug 용
    ---

    categoty 1개 조회
    """
    category = category_repository.get(db_session=db, id=category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "category search fail"},
        )

    return category


@catetory_v1_debug_router.get("", status_code=status.HTTP_200_OK, response_model=list[CategoryShowV1])
def get_all_catetory_v1_debug(db: Session = Depends(get_db)):
    """
    # Debug 용

    ---

    category 전체 목록 조회
    """
    categories = category_repository.get_multi(db_session=db)
    if len(categories) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "category search fail"},
        )

    return categories


@catetory_v1_debug_router.get(
    "/{category_id}/category-keyword", status_code=status.HTTP_200_OK, response_model=list[CategoryKeywordShowV1]
)
def get_catetory_keyword_v1_debug(category_id: int, db: Session = Depends(get_db)):
    """
    # Debug 용
    ---

    categoty 의 keyword 목록 전체 조회
    """
    category = category_repository.get(db_session=db, id=category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "category search fail"},
        )

    return category.keywords


@catetory_v1_debug_router.put(
    "/{category_id}/category-keyword", status_code=status.HTTP_201_CREATED, response_model=list[CategoryKeywordShowV1]
)
def bulk_udpate_catetory_keywords_v1_debug(
    category_id: int, keywords: list[CategoryKeywordCreate], db: Session = Depends(get_db)
):
    """
    # Debug 용
    ---

    categoty 의 keyword 목록 전체 조회
    """
    category = category_repository.get(db_session=db, id=category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"msg": "category search fail"},
        )
    bulk_udpate_catetory_keywords(db=db, category=category, keywords=keywords)
    db.refresh(category)
    return category.keywords
