import json
import os

from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session

from KsdNaverOCRServer.config import GENERAL_OCR_DOMAIN_KEY, RESULT_FILE
from KsdNaverOCRServer.config import NAVER_OCR_DOMAIN_KEY_LIST as ocr_keys
from KsdNaverOCRServer.enums import CategoryEnum
from KsdNaverOCRServer.models.ocr import OcrResult
from KsdNaverOCRServer.naver_clova.repositories import ocr_request_by_url
from KsdNaverOCRServer.schemas.ocr import ShowRequestOCR


def find_template(general_ocr_result):
    """
    general ocr 속에 domain key word를 가장 많이 포함한 domain을 찾는다
    """
    total_str = ""

    for word in general_ocr_result:
        total_str += word

    return_domain = ocr_keys[0]
    max_count = 0
    for domain in ocr_keys:
        count = 0
        for word in domain["domain_keyword_list"]:
            if word in total_str:
                count += 1
        # Todo 판단 알고리즘 변경
        # 지금은 카운드 갯수로만 비교 -> 전체 퍼센트로 변경
        if count > max_count:
            # if count / len(domain['domain_keyword_list']) > max_count_percent:
            max_count = count
            # max_count_percent = count / len(domain['domain_keyword_list'])
            return_domain = domain

    return return_domain


def request_general_ocr(
    image_url: str,
    file_name_extension: str,
):
    general_ocr_result = None
    response = ocr_request_by_url(image_url=image_url, file_name_extension=file_name_extension, category="GENERAL")
    if "images" in response:
        if response["images"][0]["inferResult"] == "SUCCESS":
            general_ocr_result = [x["inferText"] for x in response["images"][0]["fields"]]
    return general_ocr_result


def get_domain_by_image_url(
    image_url: str,
    file_name_extension: str,
):
    general_ocr_result = request_general_ocr(image_url=image_url, file_name_extension=file_name_extension)
    if general_ocr_result is None:
        return None
    return find_template(general_ocr_result)


def get_ocr_key_by_category(category: str):
    if category == GENERAL_OCR_DOMAIN_KEY["category"]:
        return GENERAL_OCR_DOMAIN_KEY
    if category == "CI":
        return ocr_keys[1]["sub_domain_list"][1]
    for ocr_key in ocr_keys:
        if ocr_key["category"] == category:
            return ocr_key


def ocr_result_filter(response):
    if response["images"][0]["inferResult"] == "SUCCESS":
        result = {}
        for field in response["images"][0]["fields"]:
            result[field["name"]] = field["inferText"]

        result_dict = {"template_name": response["images"][0]["matchedTemplate"]["name"], "results": result}
        return result_dict
    else:
        return None


def ocr_request_v2_by_url_total(user_id: str, image_url: str, file_name_extension: str, db: Session):
    ocr_key = get_domain_by_image_url(
        image_url=image_url,
        file_name_extension=file_name_extension,
    )
    request_ocr_list = []
    # Todo OCR Domain 전부 서브 도메인 양식으로 전환 예정 22.03.23
    if ocr_key is None:
        # 찾지 못해서 전체 검사 진행
        request_ocr_list = ocr_keys
    else:
        # 찾은 ocr_key만 진행
        request_ocr_list = [ocr_key]

    result_dict = []
    for ocr_key in request_ocr_list:
        request_sub_domain = [ocr_key]
        if "sub_domain_list" in ocr_key:
            request_sub_domain = ocr_key["sub_domain_list"]

        for sub_domain_key in request_sub_domain:
            response = ocr_request_by_url(
                image_url=image_url,
                file_name_extension=file_name_extension,
                category=sub_domain_key["category"],
                ocr_key=sub_domain_key,
            )

            if "images" in response:
                if response["images"][0]["inferResult"] == "SUCCESS":
                    # 도메인이 2인 경우 반환은 서브 도메인이 아닌 일반 도메인으로 반환
                    result_dict.append({"domain_ocr_key": ocr_key, "response": response})

    if len(result_dict) == 1:
        response = result_dict[0]["response"]
        ocr_key = result_dict[0]["domain_ocr_key"]
        filtered_result = ocr_result_filter(response)
        file_name = f"""{user_id}-{response['timestamp']}.json"""
        with open(RESULT_FILE + file_name, "w+") as json_file:
            json.dump(filtered_result, json_file)
        if ocr_key is None:
            print()
        new_ocr_result = OcrResult(user_id=user_id, result_file_name=file_name, category=ocr_key["category"])
        db.add(new_ocr_result)
        db.commit()
        db.refresh(new_ocr_result)

        return ShowRequestOCR(
            ocr_id=new_ocr_result.id,
            user_id=user_id,
            category=ocr_key["category"],
            created_time=new_ocr_result.created_time,
            domain_name=ocr_key["domain_name"],
            ocr_result=filtered_result,
        )

    # sub domain을 사용해 분석한 경우 요청 결과 중 하나의 결과를 선택해야함
    # 선택 알고리즘 변경 - naver ocr에서 제공하는 적중률 말고 결과 중 공백이 가장 적은 요청 선택
    elif len(result_dict) > 1:

        def get_black_count(response_dict):
            # 해당 요청의 공백 갯수를 측정
            count = 0
            field_list = response_dict["response"]["images"][0]["fields"]
            for f in field_list:
                if len(f["inferText"]) == 0:
                    count += 1
            return count

        max_result = result_dict[0]
        min_blank_count = get_black_count(response_dict=result_dict[0])
        # max_inferConfidence = result_dict[0]['response']['images'][0]['title']['inferConfidence']
        for item in result_dict:
            # 선택 알고리즘 1 - naver ocr에서 제공하는 적중율을 토대로 선택함
            # if max_inferConfidence < item['response']['images'][0]['title']['inferConfidence']:
            #     max_inferConfidence = item['response']['images'][0]['title']['inferConfidence']
            #     max_result = item
            # 선택 알고리즘 2 - 요청 결과 중 공백이 가장 적은 요청을 선택함
            if min_blank_count > get_black_count(item):
                min_blank_count = get_black_count(item)
                max_result = item

        response = max_result["response"]
        ocr_key = max_result["domain_ocr_key"]
        filtered_result = ocr_result_filter(response)
        file_name = f"""{user_id}-{response['timestamp']}.json"""
        with open(RESULT_FILE + file_name, "w+") as json_file:
            json.dump(filtered_result, json_file)

        new_ocr_result = OcrResult(user_id=user_id, result_file_name=file_name, category=ocr_key["category"])
        db.add(new_ocr_result)
        db.commit()
        db.refresh(new_ocr_result)

        return ShowRequestOCR(
            ocr_id=new_ocr_result.id,
            user_id=user_id,
            category=ocr_key["category"],
            created_time=new_ocr_result.created_time,
            domain_name=ocr_key["domain_name"],
            ocr_result=filtered_result,
        )
    else:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"OCR Template match fail \n" f"reason : {response}\n" f"ocr : {ocr_key}",
        )


def ocr_request_v2_by_url(user_id: str, image_url: str, file_name_extension: str, category: CategoryEnum, db: Session):
    ocr_key = get_ocr_key_by_category(category.value)
    response = ocr_request_by_url(
        image_url=image_url, file_name_extension=file_name_extension, category=ocr_key["category"]
    )

    if "images" in response:
        if response["images"][0]["inferResult"] == "SUCCESS":
            filtered_result = ocr_result_filter(response)
            file_name = f"""{user_id}-{response['timestamp']}.json"""
            with open(RESULT_FILE + file_name, "w+") as json_file:
                json.dump(filtered_result, json_file)

            new_ocr_result = OcrResult(user_id=user_id, result_file_name=file_name, category=ocr_key["category"])
            db.add(new_ocr_result)
            db.commit()
            db.refresh(new_ocr_result)

            return ShowRequestOCR(
                ocr_id=new_ocr_result.id,
                user_id=user_id,
                category=ocr_key["category"],
                created_time=new_ocr_result.created_time,
                domain_name=ocr_key["domain_name"],
                ocr_result=filtered_result,
            )
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"OCR Template match fail \n" f"reason : {response}"
    )


# 결과 받기
def get_ocr_result_by_OCR_ID(ocr_id: int, db: Session):
    ocr_result = db.query(OcrResult).filter(OcrResult.id == ocr_id).first()
    if not ocr_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"OCR Result with id {ocr_id} not found")

    with open(RESULT_FILE + ocr_result.result_file_name) as json_file:
        result = json.load(json_file)
    ocr_key = get_ocr_key_by_category(ocr_result.category)
    return ShowRequestOCR(
        ocr_id=ocr_result.id,
        user_id=ocr_result.user_id,
        category=ocr_result.category,
        created_time=ocr_result.created_time,
        domain_name=ocr_key["domain_name"],
        ocr_result=result,
    )


def get_ocr_result_by_user(user_id: str, db: Session):
    ocr_results = db.query(OcrResult).filter(OcrResult.user_id == user_id)
    if not ocr_results.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OCR Result not found")
    result = []
    for ocr_result in ocr_results.all():
        ocr_key = get_ocr_key_by_category(ocr_result.category)
        with open(RESULT_FILE + ocr_result.result_file_name) as json_file:
            result.append(
                ShowRequestOCR(
                    ocr_id=ocr_result.id,
                    user_id=ocr_result.user_id,
                    category=ocr_result.category,
                    domain_name=ocr_key["domain_name"],
                    created_time=ocr_result.created_time,
                    ocr_result=json.load(json_file),
                )
            )
    return result


def get_ocr_result_all(db: Session):
    result = []
    ocr_results = db.query(OcrResult).filter()
    if not ocr_results.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OCR Result not found")
    for ocr_result in ocr_results.all():
        ocr_key = get_ocr_key_by_category(ocr_result.category)
        with open(RESULT_FILE + ocr_result.result_file_name) as json_file:
            result.append(
                ShowRequestOCR(
                    ocr_id=ocr_result.id,
                    user_id=ocr_result.user_id,
                    category=ocr_result.category,
                    domain_name=ocr_key["domain_name"],
                    created_time=ocr_result.created_time,
                    ocr_result=json.load(json_file),
                )
            )
    return result


def delete_ocr_result_by_user(user_id: str, db: Session):
    ocr_results = db.query(OcrResult).filter(OcrResult.user_id == user_id)
    if not ocr_results.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OCR Result not found")

    for ocr_result in ocr_results.all():
        file_name = RESULT_FILE + ocr_result.result_file_name
        db.delete(ocr_result)
        db.commit()
        os.remove(file_name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def delete_ocr_result(ocr_id: int, db: Session):
    ocr_result = db.query(OcrResult).filter(OcrResult.id == ocr_id)
    if not ocr_result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OCR Result not found")
    file_name = ocr_result.first().result_file_name
    ocr_result.delete()
    db.commit()
    os.remove(RESULT_FILE + file_name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
