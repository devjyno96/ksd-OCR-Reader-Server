import unittest
import requests
import json

from fastapi import status

from test import user

class Order_1_OCR_Request_Test(unittest.TestCase):

    def setUp(self) -> None:
        self.host = 'http://localhost:8000/'

    def test_1_Call_OCR(self):
        ocr_request_data = {
            "s3_url": "http://s3.ap-northeast-2.amazonaws.com/ocr.image.ksd.hansung.ac.kr/1613142375245.jpg",
            "ocr_type": "D_IE",
        }
        # response = requests.post(self.host + 'ocr/', data=json.dumps(ocr_request_data))
        # response = requests.post(self.host + 'ocr/', data=ocr_request_data)
        response = requests.post(self.host + 'ocr/', json=ocr_request_data)
        print(json.loads(response.text))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Ocr Request Error")

    def test_2_test_OCR(self):
        ocr_request_data = {
            "s3_url": "https://s3.ap-northeast-2.amazonaws.com/ocr.image.ksd.hansung.ac.kr/KakaoTalk_Image_2021-08-10-22-57-58.png",
            "ocr_type": "D_IE",
        }
        response = requests.post(self.host + 'ocr/', json=ocr_request_data)
        print(json.loads(response.text))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Ocr Request Error")

    def test_3_Request_OCR_By_User(self):
        user_1 = user.get_user_list()[0]
        ocr_request_data = {
            "s3_url": "http://s3.ap-northeast-2.amazonaws.com/ocr.image.ksd.hansung.ac.kr/1613142375245.jpg",
            "ocr_type": "D_IE",
            "user_id" : user_1.id
        }
        response = requests.post(self.host + 'ocr/user', json=ocr_request_data)
        print(json.loads(response.text))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Ocr Request Error")
        pass

    def test_4_Get_OCR_Result_By_OCR_ID(self):
        pass

    def test_4_Get_OCR_Result_By_User(self):
        pass

    def test_5_Get_OCR_Result_All(self):
        pass

    def test_6_Delete_OCR_Result(self):
        pass
    #     def test_2_Get_Audit_Program(self):
    #     data = {
    #         "id": 1
    #     }
    #     response = requests.get(self.host, params=data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Audit Program Get Error")
    #
    # def test_3_Update_Audit_Program(self):
    #     audit_data = {
    #         "id": "1",
    #         "name": "audit_1",
    #         "due_date": "2021-05-10T08:30:28.573Z",
    #         "possible_results": "audit_1",
    #         "from_date": "2021-05-10T08:30:28.573Z",
    #         "to_date": "2021-05-10T08:30:28.573Z",
    #     }
    #     response = requests.put(self.host, data=json.dumps(audit_data))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Control Attribute Create Error")
    #
    # def test_4_Create_Audit_Program_all(self):
    #     audit_data = {
    #         "name": "audit_2",
    #         "due_date": "2021-05-10T08:30:28.573Z",
    #         "possible_results": "audit_2",
    #         "from_date": "2021-05-10T08:30:28.573Z",
    #         "to_date": "2021-05-10T08:30:28.573Z",
    #     }
    #     response = requests.post(self.host, data=json.dumps(audit_data))
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Audit Program Create Error")
    #     audit_data = {
    #         "name": "audit_3",
    #         "due_date": "2021-05-10T08:30:28.573Z",
    #         "possible_results": "audit_3",
    #         "from_date": "2021-05-10T08:30:28.573Z",
    #         "to_date": "2021-05-10T08:30:28.573Z",
    #     }
    #     response = requests.post(self.host, data=json.dumps(audit_data))
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg="Audit Program Create Error")
    #
    # def test_5_Delete_Audit_Program(self):
    #     audit_data = {
    #         "name": "audit_4",
    #         "due_date": "2021-05-10T08:30:28.573Z",
    #         "possible_results": "audit_4",
    #         "from_date": "2021-05-10T08:30:28.573Z",
    #         "to_date": "2021-05-10T08:30:28.573Z",
    #     }
    #     response = requests.post(self.host, data=json.dumps(audit_data))
    #     response_data = json.loads(response.text)
    #     data = {
    #         'id': response_data['id']
    #     }
    #     response = requests.delete(self.host, params=data)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg="Audit Program Delete Error")
    #
    # def test_6_Get_Audit_Program_All(self):
    #     response = requests.get(self.host + "all/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK, msg="Audit Program Get All Error")
    #


if __name__ == "__main__":
    unittest.main(warnings='ignore')