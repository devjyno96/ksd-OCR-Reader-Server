import asyncio

from sqlalchemy.orm import Session

from app.category.models import Category
from app.category.repositories import category_repository
from app.naver_clova_ocr.repositories import NaverOCRRepository
from app.naver_clova_ocr.schemas import ClovaOCRResponseV3, ImageField
from app.ocr.models import CategoryOCR
from app.ocr.repositories import general_ocr_repository


async def process_general_ocr(db_session: Session, image_url: str, image_format: str) -> ClovaOCRResponseV3 | None:
    """일반 OCR을 처리합니다."""
    general_ocr = general_ocr_repository.get_multi(db_session=db_session)[0]
    if general_ocr is None:
        return None
    result = await NaverOCRRepository().request_ocr_to_naver_clova_api(
        image_url=image_url, image_format=image_format, naver_clova_ocr=general_ocr
    )

    return result


async def process_category_ocr(
    image_url: str, image_format: str, categories: list[Category]
) -> tuple[ClovaOCRResponseV3, Category]:
    """카테고리 OCR을 처리하고, 가장 적합한 CategoryOCR을 반환합니다."""

    category_ocr_configs: list[CategoryOCR] = []
    for category in categories:
        category_ocr_configs.extend(category.category_ocr_configs)

    naver_ocr_repo = NaverOCRRepository()

    tasks = [
        naver_ocr_repo.request_ocr_to_naver_clova_api(
            image_url=image_url,
            image_format=image_format,
            naver_clova_ocr=config,
        )
        for config in category_ocr_configs
    ]
    results = await asyncio.gather(*tasks)

    # 가장 높은 평균 정확도를 가진 결과 찾기
    has_table_only = False
    best_index: int = max(
        range(len(results)),
        key=lambda i: calculate_average_confidence(results[i], has_table_only=has_table_only),
    )
    best_result = results[best_index]
    best_category_ocr = category_ocr_configs[best_index]

    return best_result, best_category_ocr.category


def calculate_average_confidence(response: ClovaOCRResponseV3, has_table_only: bool = False) -> float:
    """
    OCR 응답의 평균 정확도를 계산합니다.
    :param response: ClovaOCRResponseV3 객체
    :param has_table_only: True일 경우 table confidence만 고려, False일 경우 cell confidence 포함
    :return: 평균 정확도
    """
    if not response.images:
        return 0.0

    if not response.is_successed:
        return 0.0

    total_image_fields: list[ImageField] = []
    for image in response.images:
        total_image_fields.append(image.title)

        if not has_table_only:
            total_image_fields.extend(image.fields)

    total_confidence = sum(image_field.inferConfidence for image_field in total_image_fields)
    total_count = len(total_image_fields)
    return total_confidence / total_count if total_count > 0 else 0.0


def find_best_matching_category(db_session: Session, clova_ocr_response_v3: ClovaOCRResponseV3) -> list[Category]:
    """추출된 텍스트에서 가장 일치하는 카테고리를 찾습니다."""
    # OCR 응답에서 키워드 추출
    result_keywords = [fields.inferText for fields in clova_ocr_response_v3.images[0].fields]

    # 데이터베이스에서 카테고리 목록 조회
    categories = category_repository.get_multi(db_session=db_session)

    # 각 카테고리와 유사도 점수를 계산하고 정렬
    sorted_categories = sorted(
        categories,
        key=lambda category: calculate_similarity(category.category_keywords, result_keywords),
        reverse=True,  # 높은 점수 순으로 정렬
    )

    # 가장 높은 점수를 가진 카테고리 반환
    return sorted_categories[0:3] if sorted_categories else []


def calculate_similarity(category_keywords: list[str], target_keywords: list[str]):
    """텍스트와 키워드 간의 유사도를 계산합니다."""
    category_keywords = set(category_keywords)
    target_keywords = set(target_keywords)
    intersection = category_keywords & target_keywords

    return len(intersection) / len(target_keywords) if target_keywords else 0
