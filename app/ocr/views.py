from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.core import get_db
from app.ocr.schemas import OCRResponse
from app.ocr.services import find_best_matching_category, process_category_ocr, process_general_ocr

ocr_router_v4 = APIRouter(prefix="/v4")


@ocr_router_v4.post("/ocr", response_model=OCRResponse)
async def process_image_view(image_url: str, image_format: str, db_session: Session = Depends(get_db)):
    """이미지 URL을 받아 OCR 처리를 합니다."""
    general_result = await process_general_ocr(db_session, image_url, image_format)

    if general_result is None:
        return "general ocr result is None -> Error"

    category = find_best_matching_category(db_session, general_result)

    category_result = await process_category_ocr(image_url=image_url, image_format=image_format, category=category)

    return OCRResponse(category_result=category_result)
