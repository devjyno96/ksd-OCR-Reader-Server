import requests
import uuid
import time
import json
from KsdNaverOCRServer.config import GENERAL_OCR_DOMAIN_KEY
from KsdNaverOCRServer.repository.ocr import ocr_request_by_url

"""
도메인 이름과 해당 도메인에 있는 단어들 저장할 수 있는 도메인 클래스 선언
"""


class Domain:
    def __init__(self, sectionName, inWord):
        self.sectionName = sectionName
        self.inWord = inWord


"""
도메인에 따른 인스턴스 생성
"""
domain1 = Domain("의학적 검진", ["MRI", "Brain", "Blood", "BLOOD", "blood", "urine", "URINE", "Urine f-MRI", "f-MRI"])
domain2 = Domain("발달 및 지능 검사",
                 ["인지처리지표", "유동성-결정성지표", "FCI인지발달지수", "발달척도", "Gross motor", "순차처리전체지능", "전체 전체척도", "FSIQ", "전체지능지수",
                  "지능지수", "전체IQ", "Full Scale IQ"])
domain3 = Domain("의학적 검진", ["SELSI", "PRES", "수용언어", "전반적 언어", "표현언어"])
domain4 = Domain("사회성 및 자폐검사",
                 ["사회 적응지수", "SQ", "적응행동조합점수", "K-Vineland-II", "K-Vineland-2", "CARS", "ADOS-2", "ADI-R", "ABC",
                  "SCQ"])
domain5 = Domain("주의력 및 신경인지검사",
                 ["CCTT", "STROOP", "ATA", "주의력", "색상", "Color", "COLOR", "KIMS", "K-AVLT", "K-CFT", "전두엽", "관리지수",
                  "기억지수", "MQ", "EIQ"])
domain6 = Domain("학습검사", ["CLT", "연산성취도", "연산관련 인지처리", "연산관련", "연산", "읽기 성취도", "읽기관련 인지처리", "읽기관련", "읽기"])
domain7 = Domain("기질,성격,정서검사", ["J-TCI", "TCI", "자극추구", "NS", "불안", "우울", "ANX", "DEP", "MMPI"])

domains = [domain1, domain2, domain3, domain4, domain5, domain6, domain7]


def find_template(extractInferText):
    """
    matchDomain 변수를 선언하여 해당 json파일에 대해 match 되는 domain이 있는지 확인
    3중 for문은 오래 걸리니 뽑은 text(extractInferText)가 특정 도메인을 검증하는 단어가 맞다면
    matchDomain 값을 sectionName으로 주고 exception을 발생시켜 한번에 3중 for문 나오기
    """
    matchDomain = -1
    try:
        # domain 개수 만큼 반복
        for i in domains:
            # inWord 개수 만큼 반복
            for j in i.inWord:
                # extractInferText 개수 만큼 반복
                for k in extractInferText:
                    if (j in k):
                        print("가지고 있는 단어: " + j)
                        matchDomain = i.sectionName
                        raise NotImplementedError
    except:
        print("매칭 성공: " + matchDomain + " 영역")
    if (matchDomain == -1):
        print("match 되는 템플릿 없음")


def request_general_ocr(image_url: str, file_name_extension: str, ):
    general_ocr_result = None
    response = ocr_request_by_url(image_url=image_url, file_name_extension=file_name_extension, category='GENERAL')
    if 'images' in response:
        if response['images'][0]['inferResult'] == 'SUCCESS':
            general_ocr_result = [x['inferText'] for x in response['images'][0]['fields']]
    return general_ocr_result
