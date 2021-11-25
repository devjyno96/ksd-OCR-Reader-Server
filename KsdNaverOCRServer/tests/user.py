import unittest
import requests
import json

from fastapi import status

from KsdNaverOCRServer.models import user as user_models
from KsdNaverOCRServer.models import manage
import KsdNaverOCRServer.database

from fastapi import status

# Test code에서 사용하는 유저 리스트 받아오는 함수
def get_user_list():
    db = KsdNaverOCRServer.database.SessionLocal()
    manage.create_all()  # 초기화 매핑
    user_list = db.query(user_models.User).all()
    return user_list


class Order_1_User_Test(unittest.TestCase):

    def setUp(self) -> None:
        self.host = 'http://localhost:8000/'

    def test_1_Create_User(self):
        for i in range(1, 5):
            create_user_data = {
                "username": f"test_{i}",
                "password": "tests",
                "first_name": "tests",
                "last_name": f"_{i}",
                "is_admin": False
            }
            response = requests.post(self.host + 'user/', data=json.dumps(create_user_data))
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Create User Error")

    def test_2_Get_User(self):
        for i in range(1, 5):
            identifier_name = {'username': f'test_{i}'}
            response = requests.get(self.host + 'user/identifier', params=identifier_name)
            self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Get User Error")

    def test_3_Update_User(self):
        pass

    def test_4_Delete_User(self):
        for i in range(1, 5):
            response = requests.delete(self.host + f'user/{i}')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg="Delete User Error")


def test_6_Profile_Create(self):
    pass
    # 프로필은 나중에 구현


if __name__ == "__main__":
    unittest.main(warnings='ignore')
