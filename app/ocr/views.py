from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.category.schemas import OCRShowV3, RequestOCRV3
from app.database.core import get_db
from app.ocr.services import find_best_matching_category, process_category_ocr, process_general_ocr

ocr_router_v4 = APIRouter(prefix="/v4")


@ocr_router_v4.post("/ocr", status_code=status.HTTP_201_CREATED, response_model=OCRShowV3)
async def process_image_view(request_body: RequestOCRV3, db_session: Session = Depends(get_db)):
    """이미지 URL을 받아 OCR 처리를 합니다."""
    general_result = await process_general_ocr(db_session, request_body.image_url, request_body.file_name_extension)

    if general_result is None:
        return "general ocr result is None -> Error"

    category = find_best_matching_category(db_session, general_result)

    category_result = await process_category_ocr(
        image_url=request_body.image_url, image_format=request_body.file_name_extension, category=category
    )

    return OCRShowV3(category=category.name, domain_name=category.description, result=category_result)
