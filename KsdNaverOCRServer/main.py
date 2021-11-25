from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from KsdNaverOCRServer.models import manage
from KsdNaverOCRServer.routers import ocr, user

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

manage.create_all()

app.include_router(ocr.router)
app.include_router(user.router)
