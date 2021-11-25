from sqlalchemy import MetaData

from KsdNaverOCRServer.models import user, ocr
from KsdNaverOCRServer.database import engine, get_db


def create_all():
    user.Base.metadata.create_all(bind=engine)
    ocr.Base.metadata.create_all(bind=engine)


def delete_all():
    user.Base.metadata.drop_all(bind=engine)
    ocr.Base.metadata.drop_all(bind=engine)
