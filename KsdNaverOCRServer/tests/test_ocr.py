import asyncio
import json
import re
from datetime import datetime

from asgiref.sync import async_to_sync, sync_to_async
from fastapi import status

from KsdNaverOCRServer.config import RESOURCE_DIR
from KsdNaverOCRServer.enums import CategoryEnum
from KsdNaverOCRServer.repository.ocr import find_template, request_general_ocr
from KsdNaverOCRServer.schemas.ocr import RequestOCRByUser
from KsdNaverOCRServer.tests.base import BaseTest


class Order_1_OCR_Request_Test(BaseTest):
    def setUp(self) -> None:
        self.host = "http://localhost:8000/"

        image_file_list_json = RESOURCE_DIR + "/ivory_sample_22_03_26_v2.json"
        with open(image_file_list_json) as st_json:
            self.image_file_list = json.load(st_json)

    def _get_now_time_str(self) -> str:
        return datetime.now().strftime("%y-%m-%d %H-%M")

    def test_ocr_request_v2_by_url_total_and_delete(self):
        request_data = RequestOCRByUser(
            image_url="https://s3.ap-northeast-2.amazonaws.com/ivory.ksd.ocr.s3/test.JPG",
            file_name_extension="jpg",
            category=CategoryEnum.Total,
            user_id="test",
        )
        response = self.test_client.post("/ocr/url/v2", data=request_data.json()).json()
        self.assertIsNotNone(response["category"], msg="test_ocr_request_v2_by_url_total")

        response = self.test_client.delete("/ocr/result", params={"ocr_id": response["ocr_id"]})
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT, msg="test_ocr_request_v2_by_url_total_and_delete"
        )

    def test_ocr_request_v2_by_url_and_delete(self):
        request_data = RequestOCRByUser(
            image_url="https://s3.ap-northeast-2.amazonaws.com/ivory.ksd.ocr.s3/test.JPG",
            file_name_extension="jpg",
            category=CategoryEnum.Development_Intelligence,
            user_id="test",
        )
        response = self.test_client.post("/ocr/url/v2", data=request_data.json()).json()
        self.assertIsNotNone(response["category"], msg="test_ocr_request_v2_by_url_total")

        response = self.test_client.delete("/ocr/result", params={"ocr_id": response["ocr_id"]})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg="test_ocr_request_v2_by_url_and_delete")

    def test_get_ocr_result_by_OCR_ID(self):
        request_data = RequestOCRByUser(
            image_url="https://s3.ap-northeast-2.amazonaws.com/ivory.ksd.ocr.s3/test.JPG",
            file_name_extension="jpg",
            category=CategoryEnum.Development_Intelligence,
            user_id="test",
        )
        created_ocr = self.test_client.post("/ocr/url/v2", data=request_data.json()).json()

        response = self.test_client.get("/ocr/result", params={"ocr_id": created_ocr["ocr_id"]}).json()
        self.assertEqual(response, created_ocr, msg="test_get_ocr_result_by_OCR_ID")

        self.test_client.delete("/ocr/result", params={"ocr_id": response["ocr_id"]})

    def test_get_ocr_result_by_user(self):
        request_data = RequestOCRByUser(
            image_url="https://s3.ap-northeast-2.amazonaws.com/ivory.ksd.ocr.s3/test.JPG",
            file_name_extension="jpg",
            category=CategoryEnum.Development_Intelligence,
            user_id="test_1",
        )
        created_ocr = self.test_client.post("/ocr/url/v2", data=request_data.json()).json()

        response = self.test_client.get("/ocr/result/user", params={"user_id": created_ocr["user_id"]}).json()
        self.assertEqual(response[0]["ocr_result"], created_ocr["ocr_result"], msg="test_get_ocr_result_by_user")

        self.test_client.delete("/ocr/result", params={"ocr_id": created_ocr["ocr_id"]})

    def test_delete_ocr_result_by_user(self):
        request_data = RequestOCRByUser(
            image_url="https://s3.ap-northeast-2.amazonaws.com/ivory.ksd.ocr.s3/test.JPG",
            file_name_extension="jpg",
            category=CategoryEnum.Development_Intelligence,
            user_id="test_2",
        )
        self.test_client.post("/ocr/url/v2", data=request_data.json())
        self.test_client.post("/ocr/url/v2", data=request_data.json())

        self.test_client.delete("/ocr/result/user", params={"user_id": request_data.user_id})

        response = self.test_client.get("/ocr/result/user", params={"user_id": request_data.user_id}).json()
        self.assertEqual(response["detail"], "OCR Result not found", msg="test_delete_ocr_result_by_user")

    def test_request_general_ocr(self):
        general_image_url = (
            "https://s3.ap-northeast-2.amazonaws.com/ivory.ksd.ocr.s3/images/2.%E1%84%8B%E1%85%B5%E1%86%AB%E1%84%8C%E1%85%B5%E1%84%86%E1%85%B5%E1%86%BE%E1%84%8C%E1%85%B5%E1%84%82%E1%85%B3%E1%86%BC%E1%84%80%E1%85%A5%E1%86%B7%E1%84%89%E1%85%A1/2-11.+%E1%84%87%E1%85%A1%E1%86%AF%E1%84%83%E1%85%A1%E1%86%AF+%E1%84%86%E1%85%B5%E1%86%BE+%E1%84%8C%E1%85%B5%E1%84%82%E1%85%B3%E1%86%BC_%E1%84%8B%E1%85%B3%E1%86%AB%E1%84%91%E1%85%A7%E1%86%BC%E1%84%89%E1%85%A5%E1%86%BC%E1%84%86%E1%85%A9+%E1%84%87%E1%85%A6%E1%84%8B%E1%85%B5%E1%86%AF%E1%84%85%E1%85%B5+(1).PNG",
        )
        file_name_extension = "PNG"

        result = request_general_ocr(image_url=general_image_url, file_name_extension=file_name_extension)
        self.assertIsNotNone(result, msg="test_request_general_ocr")

    def test_all_image_request_general_ocr(self):
        with open(RESOURCE_DIR + "/image_file_list_4.json") as st_json:
            image_file_list = json.load(st_json)

        result = {}
        for image in image_file_list:
            response = request_general_ocr(
                image_url=image["url"], file_name_extension=image["url"].split(".")[-1].lower()
            )

            folder_name = image["image_name"].split("/")[1]
            image_name = image["image_name"].split("/")[2]

            if folder_name not in result:
                result[folder_name] = {}
            result[folder_name][image_name] = response

        result_file_name = "22_03_17_01"
        with open(RESOURCE_DIR + f"image_general_ocr_result_{result_file_name}.json", "w", encoding="utf-8") as fp:
            fp.write(json.dumps(result, ensure_ascii=False))

    def test_all_images_find_template(self):
        with open(RESOURCE_DIR + "image_general_ocr_result_22_03_26_02.json") as fp:
            image_general_ocr_result = json.load(fp)

        result = []
        count = 0
        total = 0
        for folder_name in image_general_ocr_result.keys():
            for image_name in image_general_ocr_result[folder_name]:
                total += 1
                if image_general_ocr_result[folder_name][image_name] is None:
                    count += 1
                    print(f"General OCR Error : {folder_name}/{image_name}")
                    result.append(
                        {
                            "expected": folder_name,
                            "result": image_general_ocr_result[folder_name][image_name],
                            "image_name": image_name,
                        }
                    )
                    continue

                result_template = find_template(image_general_ocr_result[folder_name][image_name])
                if folder_name[0] != result_template["domain_description"][0]:
                    print(f'expected :{result_template["domain_description"]} | actual : {folder_name}/{image_name}')
                    count += 1
                result.append(
                    {
                        "expected": folder_name,
                        "result": result_template,
                        "image_name": image_name,
                    }
                )
        print(f"{count} / {total}")
        with open(RESOURCE_DIR + "image_find_template_22_03_26_01.json", "w", encoding="utf-8") as fp:
            fp.write(json.dumps(result, ensure_ascii=False))

    def test_template_find_error(self):
        with open(RESOURCE_DIR + "/image_general_ocr_result_7.json") as fp:
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
                        image_general_ocr_result_1[folder_name][image_name]
                    )
                result_str_list += image_general_ocr_result_1[folder_name][image_name]

            re_numbers = re.compile(r"\d")

            result.append(
                {
                    "domain": folder_name,
                    "숫자제거합집합": [
                        x for x in list(set(result_str_list)) if re_numbers.search(x) is None and len(x) > 1
                    ],
                }
            )
        with open(RESOURCE_DIR + "template_find_2.json", "w", encoding="utf-8") as fp:
            fp.write(json.dumps(result, ensure_ascii=False))

    def test_all_images_ocr_request_v2_by_url_total(self):
        image_file_list_json = RESOURCE_DIR + "/image_file_list.json"
        ocr_result_json = RESOURCE_DIR + "image_ocr_result_7.json"
        ocr_result_format_json = RESOURCE_DIR + "image_ocr_result_formatting_4.json"
        with open(image_file_list_json) as st_json:
            image_file_list = json.load(st_json)

        result = {}
        for image in image_file_list:
            # if image['image_name'] != 'images/2.인지및지능검사/2-10. 지능검사_강남세브란스 WAIS.png':
            #     continue
            if image["image_name"].split("/")[1][0] != "2":
                continue
            request_data = RequestOCRByUser(
                image_url=image["url"],
                file_name_extension=image["image_name"].split(".")[-1],
                category=CategoryEnum.Total,
                user_id="test_test_all_images_ocr_request_v2_by_url_total",
            )
            # response = self.test_client.post('/ocr/url/v2', data=request_data.json()).json()
            import requests

            response = requests.post("http://13.125.226.39:8000/ocr/url/v2", data=request_data.json()).json()

            folder_name = image["image_name"].split("/")[1]
            image_name = image["image_name"].split("/")[2]

            if folder_name not in result:
                result[folder_name] = {}
            result[folder_name][image_name] = response
            print(f"{image['image_name']} save Complete")

        with open(ocr_result_json, "w", encoding="utf-8") as fp:
            fp.write(json.dumps(result, ensure_ascii=False))

        with open(ocr_result_json, encoding="utf-8") as fp:
            json_data = json.load(fp)
        result = {}
        for domain_name in json_data:
            if domain_name not in result:
                result[domain_name] = {}
            for image_name in json_data[domain_name]:
                if "ocr_result" in json_data[domain_name][image_name]:
                    result[domain_name][image_name] = json_data[domain_name][image_name]["ocr_result"]
                else:
                    result[domain_name][image_name] = json_data[domain_name][image_name]

        with open(ocr_result_format_json, "w", encoding="utf-8") as fp:
            fp.write(json.dumps(result, ensure_ascii=False))

    def test_aws_server_all_images_ocr_request_v2_by_url_total_v2(self):
        result_file_name = self._get_now_time_str()
        ocr_result_json = RESOURCE_DIR + f"image_ocr_result_aws_v2_{result_file_name}.json"
        ocr_result_format_json = RESOURCE_DIR + f"image_ocr_result_formatting_aws__v2{result_file_name}.json"

        result = {}
        for domain_name in self.image_file_list:
            if domain_name != "5.주의력 및 신경인지검사":
                continue
            for image in self.image_file_list[domain_name]:
                request_data = RequestOCRByUser(
                    image_url=image["url"],
                    file_name_extension=image["url"].split(".")[-1],
                    category=CategoryEnum.Total,
                    user_id="test_test_all_images_ocr_request_v2_by_url_total",
                )
                response = self.test_client.post("/ocr/url/v2", data=request_data.json()).json()

                folder_name = image["key"].split("/")[0]
                image_name = image["key"].split("/")[1]

                if folder_name not in result:
                    result[folder_name] = {}
                result[folder_name][image_name] = response
                print(f"{image['key']} save Complete")

        with open(ocr_result_json, "w", encoding="utf-8") as fp:
            fp.write(json.dumps(result, ensure_ascii=False))

        with open(ocr_result_json, encoding="utf-8") as fp:
            json_data = json.load(fp)
        result = {}
        for domain_name in json_data:
            if domain_name not in result:
                result[domain_name] = {}
            for image_name in json_data[domain_name]:
                if "ocr_result" in json_data[domain_name][image_name]:
                    result[domain_name][image_name] = json_data[domain_name][image_name]["ocr_result"]
                else:
                    result[domain_name][image_name] = json_data[domain_name][image_name]

        with open(ocr_result_format_json, "w", encoding="utf-8") as fp:
            fp.write(json.dumps(result, ensure_ascii=False))

    def test_aws_server_all_images_ocr_request_v2_by_url_total_v2_async(self):
        result_file_name = self._get_now_time_str()
        ocr_result_json = RESOURCE_DIR + f"image_ocr_result_aws_v2_{result_file_name}.json"
        ocr_result_format_json = RESOURCE_DIR + f"image_ocr_result_formatting_aws__v2{result_file_name}.json"

        result = {}
        async_list = []
        for domain_name in self.image_file_list:
            if domain_name != "7.학습검사":
                continue
            for image in self.image_file_list[domain_name]:
                request_data = RequestOCRByUser(
                    image_url=image["url"],
                    file_name_extension=image["url"].split(".")[-1],
                    category=CategoryEnum.Total,
                    user_id="test_test_all_images_ocr_request_v2_by_url_total",
                )

                def _to_async(request_data_in_func, image_in_func):
                    response = self.test_client.post("/ocr/url/v2", data=request_data_in_func.json()).json()

                    folder_name = image_in_func["key"].split("/")[0]
                    image_name = image_in_func["key"].split("/")[1]

                    if folder_name not in result:
                        result[folder_name] = {}
                    result[folder_name][image_name] = response
                    print(f"{image_in_func['key']} save Complete")

                async_list.append(sync_to_async(_to_async)(request_data, image))
        async_to_sync(asyncio.gather)(*async_list)

        with open(ocr_result_json, "w", encoding="utf-8") as fp:
            fp.write(json.dumps(result, ensure_ascii=False))

        with open(ocr_result_json, encoding="utf-8") as fp:
            json_data = json.load(fp)
        result = {}
        for domain_name in json_data:
            if domain_name not in result:
                result[domain_name] = {}
            for image_name in json_data[domain_name]:
                if "ocr_result" in json_data[domain_name][image_name]:
                    result[domain_name][image_name] = json_data[domain_name][image_name]["ocr_result"]
                else:
                    result[domain_name][image_name] = json_data[domain_name][image_name]

        with open(ocr_result_format_json, "w", encoding="utf-8") as fp:
            fp.write(json.dumps(result, ensure_ascii=False))

    def test_all_image_request_general_ocr_v2(self):
        result_file_name = self._get_now_time_str()

        result = {}
        for domain in self.image_file_list:
            for image in self.image_file_list[domain]:
                response = request_general_ocr(
                    image_url=image["url"], file_name_extension=image["key"].split(".")[-1].lower()
                )

                folder_name = image["key"].split("/")[0]
                image_name = image["key"].split("/")[1]

                if folder_name not in result:
                    result[folder_name] = {}
                result[folder_name][image_name] = response
                print(f"general ocr request complete : {image['key']}", response)

        with open(RESOURCE_DIR + f"image_general_ocr_result_{result_file_name}.json", "w", encoding="utf-8") as fp:
            fp.write(json.dumps(result, ensure_ascii=False))

    def test_template_find_error_v2(self):
        with open(RESOURCE_DIR + "/image_general_ocr_result_22_03_26_02.json") as fp:
            image_general_ocr_result_1 = json.load(fp)

        result = []
        for folder_name in image_general_ocr_result_1.keys():
            result_str_list = []
            intersection_result_str_list = []
            for image_name in image_general_ocr_result_1[folder_name]:
                if len(intersection_result_str_list) == 0:
                    intersection_result_str_list = set(image_general_ocr_result_1[folder_name][image_name])
                else:
                    try:
                        set(image_general_ocr_result_1[folder_name][image_name])
                        intersection_result_str_list = intersection_result_str_list & set(
                            image_general_ocr_result_1[folder_name][image_name]
                        )
                    except Exception as e:
                        print(e)
                result_str_list += image_general_ocr_result_1[folder_name][image_name]

            re_numbers = re.compile(r"\d")

            result.append(
                {
                    "domain": folder_name,
                    "숫자제거합집합": [
                        x for x in list(set(result_str_list)) if re_numbers.search(x) is None and len(x) > 2
                    ],
                }
            )
            for item in result:
                item["숫자제거합집합"] = list(set(item["숫자제거합집합"]))
        with open(RESOURCE_DIR + "/image_general_ocr_result_22_03_26_03_test.json", "w", encoding="utf-8") as fp:
            fp.write(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    Order_1_OCR_Request_Test.main(warnings="ignore")
