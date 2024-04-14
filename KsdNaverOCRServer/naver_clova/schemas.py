from typing import List, Optional

from pydantic import BaseModel


class Vertices(BaseModel):
    x: float
    y: float


class BoundingPoly(BaseModel):
    vertices: List[Vertices]


class TableCell(BaseModel):
    cellTextLines: List[str]
    boundingPoly: BoundingPoly
    inferConfidence: float
    rowSpan: int
    rowIndex: int
    columnSpan: int
    columnIndex: int


class ImageTable(BaseModel):
    cells: List[TableCell]
    boundingPoly: BoundingPoly
    inferConfidence: float


class SubField(BaseModel):
    boundingPoly: BoundingPoly
    inferText: str
    inferConfidence: float
    lineBreak: Optional[bool] = False


class ImageField(BaseModel):
    name: Optional[str] = None
    valueType: Optional[str] = None
    inferText: str
    inferConfidence: float
    boundingPoly: BoundingPoly
    type: Optional[str] = None
    subFields: List[SubField] = []
    checked: Optional[bool] = None
    lineBreak: Optional[bool] = None


class MatchedTemplate(BaseModel):
    id: int
    name: str


class ValidationResult(BaseModel):
    result: str
    message: Optional[str] = None


class ConvertedImageInfo(BaseModel):
    width: int
    height: int
    pageIndex: int


class CombineResult(BaseModel):
    name: Optional[str] = None
    text: Optional[str] = None


class ImageRecognitionResult(BaseModel):
    uid: str
    name: str
    inferResult: str
    message: str
    matchedTemplate: Optional[MatchedTemplate] = None
    title: Optional[ImageField] = None
    fields: List[ImageField] = []
    validationResult: Optional[ValidationResult] = None
    convertedImageInfo: Optional[ConvertedImageInfo] = None
    combineResult: Optional[CombineResult] = None
    tables: List[ImageTable] = []


class OCRResponseV2(BaseModel):
    images: List[ImageRecognitionResult]
    requestId: str
    timestamp: int
    version: str
