import unittest
from datetime import datetime

from fastapi.testclient import TestClient

from KsdNaverOCRServer import database
from KsdNaverOCRServer.main import app

test_client = TestClient(app)


# Test에서 사용할 공통 함수 및 인자를 여기서 정의해줌
class BaseTest(unittest.TestCase):
    host = "http://localhost:8000"
    db = database.SessionLocal()

    test_client = TestClient(app)  # Test Requests 를 담당하는 client

    @staticmethod
    def date_to_datetime(input_date):
        return datetime(input_date.year, input_date.month, input_date.day)
