from fastapi import FastAPI

# from .models import manage
from routers import ocr

app = FastAPI()

# manage.create_all()

app.include_router(ocr.router)
