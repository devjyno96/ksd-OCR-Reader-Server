from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.category.schemas import OCRShowV3, RequestOCRV3
from app.category.services import find_ocr_domains, handle_ocr_results, ocr_requests_by_image_url
from app.database.core import get_db

ocr_v3_router = APIRouter(prefix="/v3/ocr", tags=["OCR"])


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
