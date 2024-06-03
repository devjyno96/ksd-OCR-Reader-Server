from sqlalchemy.orm import Session

from app.category.models import Category
from app.category.repositories import category_repository
from app.naver_clova_ocr.repositories import NaverOCRRepository
from app.naver_clova_ocr.schemas import ClovaOCRResponseV3
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


async def process_category_ocr(image_url: str, image_format: str, category: Category) -> ClovaOCRResponseV3:
    """카테고리 OCR을 처리합니다."""

    category_ocr_configs = category.category_ocr_configs
    results = []
    for config in category_ocr_configs:
        result = await NaverOCRRepository().request_ocr_to_naver_clova_api(
            image_url=image_url, image_format=image_format, naver_clova_ocr=config
        )
        results.append(result)

    def get_blank_count(ocr_response: ClovaOCRResponseV3):
        return sum(1 for f in ocr_response.images[0].fields if len(f.inferText) == 0)

    best_result = min(results, key=get_blank_count)
    return best_result


def find_best_matching_category(db_session: Session, clova_ocr_response_v3: ClovaOCRResponseV3) -> Category | None:
    """추출된 텍스트에서 가장 일치하는 카테고리를 찾습니다."""
    result_keywords = []
    for fields in clova_ocr_response_v3.images[0].fields:
        result_keywords.append(fields.inferText)

    categories = category_repository.get_multi(db_session=db_session)

    best_match = None

    highest_score = 0
    for category in categories:
        score = calculate_similarity(category.category_keywords, result_keywords)
        if score > highest_score:
            highest_score = score
            best_match = category

    return best_match


def calculate_similarity(category_keywords: list[str], target_keywords: list[str]):
    """텍스트와 키워드 간의 유사도를 계산합니다."""
    category_keywords = set(category_keywords)
    target_keywords = set(target_keywords)
    intersection = category_keywords & target_keywords

    return len(intersection) / len(target_keywords) if target_keywords else 0
