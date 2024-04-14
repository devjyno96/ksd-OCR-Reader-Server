from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import KsdNaverOCRServer.database
from KsdNaverOCRServer.repository import user
from KsdNaverOCRServer.routers.routers_function import get_summary_location
from KsdNaverOCRServer.schemas import user as schemas

router = APIRouter(prefix="/user", tags=["User"])
get_db = KsdNaverOCRServer.database.get_db


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    deprecated=True,
    response_model=schemas.ShowUser,
    responses={
        409: {
            "description": "Error: Conflict",
        },
    },
    summary="create" + " | " + get_summary_location(),
)
def create(request: schemas.User, db: Session = Depends(get_db)):
    # router.post(summary= __name__ + get_summary(currentframe))
    """
    ### 설명
    - User 생성
    ### Request Body
    - username : User 의 아이디
    - password : User 의 패스워드
    - first_name : User 의 first name
    - last_name : User 의 last name
    - is_admin : User 의 admin 여부(true, false 둘 중 하나)
    ### 관련 모델
    - User
    """
    return user.create(request, db)


@router.get(
    "/identifier",
    status_code=status.HTTP_200_OK,
    deprecated=True,
    response_model=schemas.ShowUser,
    responses={
        404: {
            "description": "Error: Not Found",
        },
    },
    summary="check_id" + " | " + get_summary_location(),
)
def check_id(username: str, db: Session = Depends(get_db)):
    """
    ### 설명
    - username 있는지 확인
    - username 는 email(아이디)을 의미함
    ### 파라미터
    - username : User 의 아이디
    ### 관련 모델
    - User
    """

    return user.show_by_name(username, db)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    deprecated=True,
    responses={
        404: {
            "description": "Error: Not Found",
        },
    },
    summary="login" + " | " + get_summary_location(),
)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    ### 설명
    - login 확인 후 token 반환
    ### Request Body
    - username : User 의 아이디
    - password : User 의 패스워드
    - 기타 로그인 관련 파라미터들
    ### 관련 모델
    - User
    """
    return user.login(request, db)


@router.put(
    "/password",
    status_code=status.HTTP_200_OK,
    deprecated=True,
    responses={
        404: {
            "description": "Error: Not Found",
        },
    },
    summary="change_pw" + " | " + get_summary_location(),
)
def change_pw(request: schemas.ChangePassword, db: Session = Depends(get_db)):
    """
    ### 설명
    - password 변경
    ### Request Body
    - username : User 의 아이디
    - new_password : 새로운 패스워드
    - check_password: 새로운 패스워드 확인
    ### 관련 모델
    - User
    """

    return user.change_password(request, db)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    deprecated=True,
    responses={
        404: {
            "description": "Error: Not Found",
        },
    },
    summary="delete" + " | " + get_summary_location(),
)
def delete(user_id: int, db: Session = Depends(get_db)):
    """
    ### 설명
    - User 삭제
    ### 파라미터
    - user_id : User 의 ID(username 이 아닌 user_id 을 의미)
    ### 관련 모델
    - User
    """
    return user.delete(user_id, db)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")


# Profile
@router.get(
    "/profile/{user_id}",
    status_code=status.HTTP_200_OK,
    deprecated=True,
    responses={
        404: {
            "description": "Error: Not Found",
        },
    },
    summary="show_profile" + " | " + get_summary_location(),
)
def show_profile(user_id: int, db: Session = Depends(get_db)):
    """
    ### 설명
    - User profile 조회
    ### 파라미터
    - user_id : User 의 ID(username 이 아닌 user_id 을 의미)
    """
    return user.show_profile(user_id, db)


@router.post(
    "/profile/",
    status_code=status.HTTP_201_CREATED,
    deprecated=True,
    responses={
        404: {
            "description": "Error: Not Found",
        },
    },
    summary="create_profile" + " | " + get_summary_location(),
)
def create_profile(request: schemas.CreateProfile, db: Session = Depends(get_db)):
    """
    ### 설명
    - User Profile 생성
    ### Request body
    - user_id : User 의 ID(username 이 아닌 user_id 을 의미)
    - email : User가 알람을 받을 Email, 로그인 할때랑은 다른 값을 사용할 수 있음(Unique)
    - team : 소속 팀 이름
    - company : 소속 회사 이름
    - department : 소속 부서 이름,
    - title : 직책 이름,
    - phone : 핸드폰 번호
    """
    return user.create_profile(request, db)


@router.put(
    "/profile/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    deprecated=True,
    responses={
        404: {
            "description": "Error: Not Found",
        },
    },
    summary="update_profile" + " | " + get_summary_location(),
)
def update_profile(user_id: int, requests: schemas.UpdateProfile, db: Session = Depends(get_db)):
    """
    ### 설명
    - User Profile 수정
    ### 파라미터
    - user_id : User 의 ID(username 이 아닌 user_id 을 의미)
    """
    return user.update_profile(user_id, requests, db)


@router.delete(
    "/profile/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    deprecated=True,
    responses={
        404: {
            "description": "Error: Not Found",
        },
    },
    summary="delete_profile" + " | " + get_summary_location(),
)
def delete_profile(user_id: int, db: Session = Depends(get_db)):
    """
    ### 설명
    - User Profile 삭제
    ### 파라미터
    - user_id : User 의 ID(username 이 아닌 user_id 을 의미)
    """
    return user.delete_profile(user_id, db)
