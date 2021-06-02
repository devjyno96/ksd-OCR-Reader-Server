from typing import List, Optional

from pydantic import BaseModel


class RequestOCR(BaseModel):
    s3_url: str
    ocr_type: str

    # class Config():
    #     orm_mode = True
