from fastapi import status

from KsdNaverOCRServer.schemas.ocr import RequestOCRByUser
from KsdNaverOCRServer.tests.base import BaseTest
from KsdNaverOCRServer.enums import CategoryEnum
from KsdNaverOCRServer.config import ROOT_DIR


class Order_1_OCR_Request_Test(BaseTest):

    def setUp(self) -> None:
        self.host = 'http://localhost:8000/'

    def test_ocr_request_v2_by_url_total_and_delete(self):
        request_data = RequestOCRByUser(
            image_url='https://s3.ap-northeast-2.amazonaws.com/ivory.ksd.ocr.s3/test.JPG',
            file_name_extension="jpg",
            category=CategoryEnum.Total,
            user_id='test',
        )
        response = self.test_client.post('/ocr/url/v2', data=request_data.json()).json()
        self.assertIsNotNone(response['category'], msg='test_ocr_request_v2_by_url_total')

        response = self.test_client.delete('/ocr/result', params={'ocr_id': response['ocr_id']})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         msg='test_ocr_request_v2_by_url_total_and_delete')

    def test_ocr_request_v2_by_url_and_delete(self):
        request_data = RequestOCRByUser(
            image_url='https://s3.ap-northeast-2.amazonaws.com/ivory.ksd.ocr.s3/test.JPG',
            file_name_extension="jpg",
            category=CategoryEnum.Development_Intelligence,
            user_id='test',
        )
        response = self.test_client.post('/ocr/url/v2', data=request_data.json()).json()
        self.assertIsNotNone(response['category'], msg='test_ocr_request_v2_by_url_total')

        response = self.test_client.delete('/ocr/result', params={'ocr_id': response['ocr_id']})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg='test_ocr_request_v2_by_url_and_delete')

    def test_get_ocr_result_by_OCR_ID(self):
        request_data = RequestOCRByUser(
            image_url='https://s3.ap-northeast-2.amazonaws.com/ivory.ksd.ocr.s3/test.JPG',
            file_name_extension="jpg",
            category=CategoryEnum.Development_Intelligence,
            user_id='test',
        )
        created_ocr = self.test_client.post('/ocr/url/v2', data=request_data.json()).json()

        response = self.test_client.get('/ocr/result', params={'ocr_id': created_ocr['ocr_id']}).json()
        self.assertEqual(response, created_ocr, msg='test_get_ocr_result_by_OCR_ID')

        self.test_client.delete('/ocr/result', params={'ocr_id': response['ocr_id']})

    def test_get_ocr_result_by_user(self):
        request_data = RequestOCRByUser(
            image_url='https://s3.ap-northeast-2.amazonaws.com/ivory.ksd.ocr.s3/test.JPG',
            file_name_extension="jpg",
            category=CategoryEnum.Development_Intelligence,
            user_id='test_1',
        )
        created_ocr = self.test_client.post('/ocr/url/v2', data=request_data.json()).json()

        response = self.test_client.get('/ocr/result/user', params={'user_id': created_ocr['user_id']}).json()
        self.assertEqual(response[0]['ocr_result'], created_ocr['ocr_result'], msg='test_get_ocr_result_by_user')

        self.test_client.delete('/ocr/result', params={'ocr_id': created_ocr['ocr_id']})

    def test_delete_ocr_result_by_user(self):
        request_data = RequestOCRByUser(
            image_url='https://s3.ap-northeast-2.amazonaws.com/ivory.ksd.ocr.s3/test.JPG',
            file_name_extension="jpg",
            category=CategoryEnum.Development_Intelligence,
            user_id='test_2',
        )
        self.test_client.post('/ocr/url/v2', data=request_data.json())
        self.test_client.post('/ocr/url/v2', data=request_data.json())

        self.test_client.delete('/ocr/result/user', params={'user_id': request_data.user_id})

        response = self.test_client.get('/ocr/result/user', params={'user_id': request_data.user_id}).json()
        self.assertEqual(response['detail'], 'OCR Result not found', msg='test_delete_ocr_result_by_user')


if __name__ == "__main__":
    Order_1_OCR_Request_Test.main(warnings='ignore')
