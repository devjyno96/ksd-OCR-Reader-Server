from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.core import get_db
from app.ocr.schemas import OCRResponse
from app.ocr.services import find_best_matching_category, process_category_ocr, process_general_ocr

router = APIRouter()


@router.post("/ocr", response_model=OCRResponse)
async def process_image_view(image_url: str, db: Session = Depends(get_db)):
    """이미지 URL을 받아 OCR 처리를 합니다."""
    general_result = await process_general_ocr(db, image_url)

    category = find_best_matching_category(db, general_result["result"])
    category_result = await process_category_ocr(db, image_url, category.name)

    return OCRResponse(general_result=general_result, category_result=category_result)
