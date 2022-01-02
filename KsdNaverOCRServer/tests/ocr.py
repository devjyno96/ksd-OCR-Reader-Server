import json

from fastapi import status
from KsdNaverOCRServer.tests.base import BaseTest
from KsdNaverOCRServer.enums import CategoryEnum
from KsdNaverOCRServer.config import ROOT_DIR

class Order_1_OCR_Request_Test(BaseTest):

    def setUp(self) -> None:
        self.host = 'http://localhost:8000/'

    def test_1_Call_OCR(self):
        ocr_request_data = {
            "s3_url": "http://s3.ap-northeast-2.amazonaws.com/ocr.image.ksd.hansung.ac.kr/1613142375245.jpg",
            "ocr_type": "D_IE",
        }
        response = self.test_client.post(self.host + 'ocr/', json=ocr_request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Ocr Request Error")

    def test_1_1_Call_OCR_v2(self):
        filepath = ROOT_DIR + '/KsdNaverOCRServer/tests/resource/덴버발달.JPG'
        request_category = CategoryEnum.Development_Intelligence
        with open(filepath, 'rb') as fh:
            create_file = {
                'category': (None, request_category.value),
                'image_file': fh
            }
            result = self.test_client.post('/ocr/v2',
                                           files=create_file,
                                           ).json()
        print()
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Ocr Request Error")

    def test_2_test_OCR(self):
        ocr_request_data = {
            "s3_url": "https://s3.ap-northeast-2.amazonaws.com/ocr.image.ksd.hansung.ac.kr/KakaoTalk_Image_2021-08-10-22-57-58.png",
            "ocr_type": "D_IE",
        }
        response = self.test_client.post(self.host + 'ocr/v2', json=ocr_request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Ocr Request Error")

    def test_3_Request_OCR_By_User(self):
        user_1 = 1
        ocr_request_data = {
            "s3_url": "http://s3.ap-northeast-2.amazonaws.com/ocr.image.ksd.hansung.ac.kr/1613142375245.jpg",
            "ocr_type": "D_IE",
            "user_id": user_1
        }
        response = self.test_client.post(self.host + 'ocr/user', json=ocr_request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Ocr Request Error")

    def test_4_Get_OCR_Result_All(self):
        response = self.test_client.get(self.host + 'ocr/all')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Ocr Request Error")

    def test_5_Get_OCR_Result_By_OCR_ID(self):
        ocr_results = json.loads(self.test_client.get(self.host + 'ocr/all').text)

        response = self.test_client.get(self.host + 'ocr/result', params={"ocr_id": ocr_results[0]['id']})
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Ocr Request Error")

    def test_6_Get_OCR_Result_By_User(self):
        ocr_results = json.loads(self.test_client.get(self.host + 'ocr/all').text)
        response = self.test_client.get(self.host + 'ocr/result/user', params={"user_id": ocr_results[0]['user_id']})
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Ocr Request Error")

    def test_7_Delete_OCR_Result(self):
        ocr_results = json.loads(self.test_client.get(self.host + 'ocr/all').text)
        response = self.test_client.delete(self.host + 'ocr/result', params={"ocr_id": ocr_results[0]['user_id']})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg="Ocr Request Error")

    def test_8_Delete_OCR_Result_by_user(self):
        self.test_3_Request_OCR_By_User()
        ocr_results = json.loads(self.test_client.get(self.host + 'ocr/all').text)
        response = self.test_client.delete(self.host + 'ocr/result/user', params={"user_id": ocr_results[0]['user_id']})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg="Ocr Request Error")


if __name__ == "__main__":
    Order_1_OCR_Request_Test.main(warnings='ignore')
