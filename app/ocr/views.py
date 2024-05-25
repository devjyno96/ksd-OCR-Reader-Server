from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.core import get_db
from app.ocr.schemas import OCRRequest, OCRResponse
from app.ocr.services import process_image

router = APIRouter()


@router.post("/ocr", response_model=OCRResponse)
async def process_image_view(ocr_request: OCRRequest, db: Session = Depends(get_db)):
    """이미지 URL을 받아 OCR 처리를 합니다."""
    try:
        result = await process_image(db, ocr_request.image_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
