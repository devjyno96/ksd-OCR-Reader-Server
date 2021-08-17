from datetime import timedelta

from fastapi import HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError
from sqlalchemy.orm import Session

from models import user as models

from schemas import user as schemas

from hashing import Hash


def create(request: schemas.User, db: Session):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Username {request.username} is already used')
    new_user = models.User(username=request.username,
                           password=Hash.bcrypt(request.password),
                           first_name=request.first_name,
                           last_name=request.last_name,
                           is_admin=request.is_admin)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user


def show(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {id} is not available')
    return user


def show_by_name(username: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


def login(request: OAuth2PasswordRequestForm, db: Session):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Invalid Credentials')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Incorrect password')
    # generate a jwt token and return

    # generate refresh token
    Authorize = AuthJWT()
    access_token = Authorize.create_access_token(subject=user.username, expires_time=timedelta(seconds=60))
    refresh_token = Authorize.create_refresh_token(subject=user.username, expires_time=timedelta(seconds=60))

    # if token already exist in DB == delete and create token
    refresh_token_db = db.query(models.RefreshToken).filter(models.RefreshToken.user_id == user.id)
    if refresh_token_db.first():
        refresh_token_db.delete()
        db.commit()

    # refresh token create and save to DB
    refresh_token_db = models.RefreshToken(
        user_id=user.id,
        token=refresh_token
    )
    db.add(refresh_token_db)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


def change_password(request: schemas.ChangePassword, db: Session):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {id} is not available')
    if request.new_password != request.check_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Password does not matched')
    user.password = Hash.bcrypt(request.new_password)
    db.commit()
    return "done"


def delete(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {id} is not available')

    user.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def refresh_token(Authorize: AuthJWT, db: Session):
    # Refresh Token
    try:
        Authorize.jwt_refresh_token_required()
    except JWTDecodeError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Token is not Refresh Token')

    try:
        Authorize.get_raw_jwt()
    except JWTDecodeError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'Refresh Token is not available')

    # user의 refresh token이랑 jti 값이 동일한지 확인
    user = db.query(models.User).filter(models.User.username == Authorize.get_jwt_subject()).first()
    refresh_token_db = db.query(models.RefreshToken).filter(models.RefreshToken.user_id == user.id).first()

    if Authorize.get_jti(refresh_token_db.token) != Authorize.get_raw_jwt()['jti']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'Refresh Token does not Matched')

    new_access_token = Authorize.create_access_token(subject=Authorize.get_jwt_subject())

    return {"access_token": new_access_token}


#  Profile
def create_profile(request: schemas.CreateProfile, db: Session):
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'User id {request.user_id} is not exist')

    profile_email_check = db.query(models.Profile).filter(models.Profile.email == request.email).first()
    if profile_email_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'Email  {request.email}  is already exist')

    profile = models.Profile(user_id=request.user_id,
                             email=request.email,
                             team=request.team,
                             company=request.company,
                             department=request.department,
                             title=request.title,
                             phone=request.phone,
                             )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


def show_profile(user_id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {user_id} is not available')
    user_profile = db.query(models.Profile).filter(models.Profile.user_id == user.id).first()
    return user_profile


def update_profile(user_id: int, request: schemas.UpdateProfile, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {user_id} is not available')

    user_profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    if not user_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Profile with the user id {user_id} is not available')

    user_profile.email = request.email
    user_profile.team = request.team
    user_profile.company = request.company
    user_profile.department = request.department
    user_profile.title = request.title
    user_profile.phone = request.phone

    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def delete_profile(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {id} is not available')

    user_profile = db.query(models.Profile).filter(user == user).delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
