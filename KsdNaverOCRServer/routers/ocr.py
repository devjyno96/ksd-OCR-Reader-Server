from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from KsdNaverOCRServer.database import get_db
from KsdNaverOCRServer.enums import CategoryEnum
from KsdNaverOCRServer.ocr.schemas import RequestOCRV3
from KsdNaverOCRServer.repository import ocr as ocr_repository

router = APIRouter(prefix="/ocr", tags=["Ocr"])


@router.post(
    "/url/v2",
    status_code=status.HTTP_201_CREATED,
)
def ocr_request_v2_by_url(request: RequestOCRV3, db: Session = Depends(get_db)):
    """
    # 이미지 파일 url을 전달 받는 API 입니다.

    파일을 드라이브에 업로드 하고 퍼블릭 엑세스 허용을 하신 다음 해당 파일 url을 body에 담아 요청하시면 됩니다.

    해당 category에 맞게 string으로 넘겨주시면 됩니다.

    TOTAL의 경우 아래 카테고리 중 해당하는 카테고리를 찾아서 반환해 줍니다.

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
            },
            {
                "domain_description": "8. 전체 검사",
                "domain_name": "Total",
                "category": "TOTAL"
            }
        ]
    """

    if request.category == CategoryEnum.Total:
        # Todo 카테고리 분류 후 여기서 ocr_request_v2_by_url 카테고리 지정해서 요청하는 방식으로 변경(가독성 때문임) 22.03.23
        return ocr_repository.ocr_request_v2_by_url_total(
            user_id=1, image_url=request.image_url, file_name_extension=request.file_name_extension, db=db
        )
    else:
        return ocr_repository.ocr_request_v2_by_url(
            user_id=1,
            image_url=request.image_url,
            file_name_extension=request.file_name_extension,
            category=request.category,
            db=db,
        )


# 결과 받기
@router.get("/result", status_code=status.HTTP_200_OK, deprecated=True)
def get_ocr_result_by_OCR_ID(ocr_id: int, db: Session = Depends(get_db)):
    """
    OCR 분석 결과 중 해당 id의 결과 불러오기
    """
    return ocr_repository.get_ocr_result_by_OCR_ID(ocr_id, db)


@router.get("/result/user", status_code=status.HTTP_200_OK, deprecated=True)
def get_ocr_result_by_user(user_id: str, db: Session = Depends(get_db)):
    """
    OCR 분석 결과 중 해당 user id의 모든 결과 불러오기
    """
    return ocr_repository.get_ocr_result_by_user(user_id, db)


@router.get("/all", status_code=status.HTTP_200_OK, deprecated=True)
def get_ocr_result_all(db: Session = Depends(get_db)):
    """
    OCR 분석 결과 전체 불러오기
    """
    return ocr_repository.get_ocr_result_all(db)


@router.delete("/result/user", status_code=status.HTTP_204_NO_CONTENT, deprecated=True)
def delete_ocr_result_by_user(user_id: str, db: Session = Depends(get_db)):
    """
    OCR 분석 결과 중 해당 user id의 모든 결과 삭제하기
    """
    return ocr_repository.delete_ocr_result_by_user(user_id, db)


@router.delete("/result", status_code=status.HTTP_204_NO_CONTENT, deprecated=True)
def delete_ocr_result(ocr_id: int, db: Session = Depends(get_db)):
    """
    OCR 분석 결과 삭제
    """
    return ocr_repository.delete_ocr_result(ocr_id, db)
