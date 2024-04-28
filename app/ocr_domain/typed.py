from typing import TypedDict


class MedicalExaminationConfig(TypedDict):
    """
    의학적 검진 API 설정을 위한 TypedDict입니다.

    속성:
        domain_description (str): 의료 도메인에 대한 설명입니다.
        domain_name (str): 의료 도메인을 식별하는 고유 이름입니다.
        secret_key (str): API 접근 보안을 위한 비밀 키입니다.
        APIGW_Invoke_url (str): 해당 도메인의 API 게이트웨이를 호출하기 위한 URL입니다.
        category (str): 도메인을 특정 분류 아래로 분류하기 위한 카테고리 코드입니다.
        domain_keyword_list (List[str]): 도메인과 관련된 키워드 목록입니다.
    """

    domain_description: str
    domain_name: str
    secret_key: str
    APIGW_Invoke_url: str
    category: str
    domain_keyword_list: list[str]
