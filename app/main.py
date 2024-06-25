from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from sqladmin import Admin

from app.admin import authentication_backend
from app.category.admin import CategoryAdmin, CategoryKeywordAdmin
from app.category.views import ocr_v3_router
from app.database.core import engine
from app.ocr.admin import CategoryOCRAdmin, GeneralOCRAdmin
from app.ocr.views import ocr_router_v4

title = "아이보리 OCR API"
description = """
[Github Link](https://github.com/jinho9613/ksd-OCR-Reader-Server)
"""
version = "2022년 3월 23일 버전"

app = FastAPI(title=title, description=description, version=version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ocr_router_v4)
app.include_router(ocr_v3_router)



@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


# SqlAdmin Settings
admin = Admin(app, engine, authentication_backend=authentication_backend)

# Add views
admin.add_view(CategoryAdmin)
admin.add_view(CategoryKeywordAdmin)
admin.add_view(GeneralOCRAdmin)
admin.add_view(CategoryOCRAdmin)
