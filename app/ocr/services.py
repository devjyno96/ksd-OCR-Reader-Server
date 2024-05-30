from sqlalchemy.orm import Session

from app.category.models import Category
from app.category.repositories import CategoryRepository
from app.naver_clova_ocr.services import call_ocr_api
from app.ocr.repositories import GeneralOCRRepository


# TODO : 2024.05.29 여기 진행하고 있었음
async def process_general_ocr(db: Session, image_url: str):
    """일반 OCR을 처리합니다."""
    general_ocr = GeneralOCRRepository.get_multi()[0]
    result = await call_ocr_api(general_ocr.ocr_api_url, general_ocr.ocr_api_key, image_url)
    return result


async def process_category_ocr(db: Session, image_url: str, category_name: str):
    """카테고리 OCR을 처리합니다."""

    category = CategoryRepository.get_by_name(db, category_name)
    if not category:
        raise ValueError("Category not found")

    category_ocr_configs = category.category_ocr_configs
    results = []
    for config in category_ocr_configs:
        result = await call_ocr_api(config.ocr_api_url, config.ocr_api_key, image_url)
        results.append(result)
    return results


def find_best_matching_category(db: Session, text: str):
    """추출된 텍스트에서 가장 일치하는 카테고리를 찾습니다."""
    category_repository = CategoryRepository()
    categories = db.query(Category).all()
    best_match = None
    highest_score = 0
    for category in categories:
        score = calculate_similarity(text, category_repository.get_category_keywords(db, category.id))
        if score > highest_score:
            highest_score = score
            best_match = category
    if not best_match:
        raise ValueError("No matching category found")
    return best_match


def calculate_similarity(text: str, keywords):
    """텍스트와 키워드 간의 유사도를 계산합니다."""
    text_words = set(text.split())
    keyword_words = set(kw.keyword for kw in keywords)  # noqa C401
    intersection = text_words.intersection(keyword_words)
    return len(intersection) / len(keyword_words) if keyword_words else 0
