from typing import List, Optional

from pydantic import BaseModel

from KsdNaverOCRServer.enums import CategoryEnum


class RequestOCR(BaseModel):
    image_url: str
    category: CategoryEnum



class RequestOCRByUser(RequestOCR):
    user_id: int

