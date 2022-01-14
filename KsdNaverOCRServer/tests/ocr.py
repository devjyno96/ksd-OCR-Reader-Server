import json

from fastapi import status

from KsdNaverOCRServer.repository.general_ocr import request_general_ocr, find_template
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

    def test_request_general_ocr(self):
        from KsdNaverOCRServer.repository.general_ocr import request_general_ocr
        request_data = RequestOCRByUser(
            image_url='https://s3.ap-northeast-2.amazonaws.com/ivory.ksd.ocr.s3/test.JPG',
            file_name_extension="jpg",
            category=CategoryEnum.Development_Intelligence,
            user_id='test_2',
        )
        result = request_general_ocr(image_url=request_data.image_url,
                                     file_name_extension=request_data.file_name_extension)
        self.assertIsNotNone(result, msg='test_request_general_ocr')

    def test_find_template(self):
        from KsdNaverOCRServer.repository.general_ocr import request_general_ocr, find_template
        request_data = RequestOCRByUser(
            image_url='https://s3.ap-northeast-2.amazonaws.com/ivory.ksd.ocr.s3/test.JPG',
            file_name_extension="jpg",
            category=CategoryEnum.Development_Intelligence,
            user_id='test_2',
        )
        result = request_general_ocr(image_url=request_data.image_url,
                                     file_name_extension=request_data.file_name_extension)
        self.assertIsNotNone(result, msg='test_request_general_ocr')
        test = find_template(result)
        print()

    def test_test(self):
        from KsdNaverOCRServer.tests.resource.ocr_image_list_in_s3 import image_list
        image_list = image_list
        from KsdNaverOCRServer.repository.general_ocr import request_general_ocr, find_template
        request_data = RequestOCRByUser(
            image_url=image_list[0],
            file_name_extension=image_list[0].split('.')[-1],
            category=CategoryEnum.Total,
            user_id='test_2',
        )
        result = request_general_ocr(image_url=request_data.image_url,
                                     file_name_extension=request_data.file_name_extension)
        self.assertIsNotNone(result, msg='test_request_general_ocr')
        test = find_template(result)
        print()

    def test_all_image_request_general_ocr(self):
        with open(ROOT_DIR + "/KsdNaverOCRServer/tests/resource/image_file_list.json", "r") as st_json:
            image_file_list = json.load(st_json)

        result = {}
        for image in image_file_list:
            response = request_general_ocr(image_url=image['url'],
                                           file_name_extension=image['url'].split('.')[-1])
            folder_name = image['image_name'].split('/')[1]
            image_name = image['image_name'].split('/')[2]

            if folder_name not in result:
                result[folder_name] = {}
            result[folder_name][image_name] = response

        with open('image_general_ocr_result_2.json', 'w', encoding="utf-8") as fp:
            fp.write(json.dumps(result, ensure_ascii=False))

    def test_all_images_find_template(self):
        with open('image_general_ocr_result.json', 'r') as fp:
            image_general_ocr_result_1 = json.load(fp)
        with open('image_general_ocr_result_2.json', 'r') as fp:
            image_general_ocr_result_2 = json.load(fp)

        """
        [
            {
                'expected' : str,
                'result' : str,
                'image_name'
            },
            ...
        ]
        """
        result = []
        count = 0
        total = 0
        for folder_name in image_general_ocr_result_1.keys():
            for image_name in image_general_ocr_result_1[folder_name]:
                total += 1
                result_template = find_template(image_general_ocr_result_1[folder_name][image_name])
                if folder_name != result_template:
                    print(f'Not Match! | expected :{result_template} | actual : {folder_name}/{image_name}')
                    count += 1
                result.append({
                    'expected': folder_name,
                    'result': result_template,
                    'image_name': image_name,
                })
        print(f"{count} / {total}")
        with open('image_find_template.json', 'w', encoding="utf-8") as fp:
            fp.write(json.dumps(result, ensure_ascii=False))

    def test_template_find_error(self):
        with open('image_general_ocr_result.json', 'r') as fp:
            image_general_ocr_result_1 = json.load(fp)

        result = []
        for folder_name in image_general_ocr_result_1.keys():
            result_str_list = []
            intersection_result_str_list = []
            for image_name in image_general_ocr_result_1[folder_name]:
                if len(intersection_result_str_list) == 0:
                    intersection_result_str_list = set(image_general_ocr_result_1[folder_name][image_name])
                else:
                    intersection_result_str_list = intersection_result_str_list & set(
                        image_general_ocr_result_1[folder_name][image_name])
                result_str_list += image_general_ocr_result_1[folder_name][image_name]
            result.append({
                'domain': folder_name,
                '합집합': list(set(result_str_list)),
                '교집합': list(intersection_result_str_list),
            })
        with open('template_find.json', 'w', encoding="utf-8") as fp:
            fp.write(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    Order_1_OCR_Request_Test.main(warnings='ignore')
