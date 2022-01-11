from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from KsdNaverOCRServer.models import manage
from KsdNaverOCRServer.routers import ocr, user

title = "아이보리 OCR API"
description = """
[Github Link](https://github.com/jinho9613/ksd-OCR-Reader-Server)
"""
version = "2022년 1월 12일 버전"

app = FastAPI(
    title=title,
    description=description,
    version=version
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manage.create_all()

app.include_router(ocr.router)
# app.include_router(user.router)
