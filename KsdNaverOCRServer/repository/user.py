from datetime import timedelta

from fastapi import HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from KsdNaverOCRServer.hashing import Hash
from KsdNaverOCRServer.models import user as models
from KsdNaverOCRServer.schemas import user as schemas


def create(request: schemas.User, db: Session):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Username {request.username} is already used")
    new_user = models.User(
        username=request.username,
        password=Hash.bcrypt(request.password),
        first_name=request.first_name,
        last_name=request.last_name,
        is_admin=request.is_admin,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def show(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
    return user


def show_by_name(username: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


def login(request: OAuth2PasswordRequestForm, db: Session):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
    # generate a jwt token and return

    # generate refresh token
    Authorize = AuthJWT()  # noqa F841
    access_token = Authorize.create_access_token(subject=user.username, expires_time=timedelta(seconds=60))
    refresh_token = Authorize.create_refresh_token(subject=user.username, expires_time=timedelta(seconds=60))

    # if token already exist in DB == delete and create token
    refresh_token_db = db.query(models.RefreshToken).filter(models.RefreshToken.user_id == user.id)
    if refresh_token_db.first():
        refresh_token_db.delete()
        db.commit()

    # refresh token create and save to DB
    refresh_token_db = models.RefreshToken(user_id=user.id, token=refresh_token)
    db.add(refresh_token_db)
    db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


def change_password(request: schemas.ChangePassword, db: Session):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
    if request.new_password != request.check_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password does not matched")
    user.password = Hash.bcrypt(request.new_password)
    db.commit()
    return "done"


def delete(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")

    user.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#  Profile
def create_profile(request: schemas.CreateProfile, db: Session):
    user = db.query(models.User).filter(models.User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User id {request.user_id} is not exist")

    profile_email_check = db.query(models.Profile).filter(models.Profile.email == request.email).first()
    if profile_email_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email  {request.email}  is already exist")

    profile = models.Profile(
        user_id=request.user_id,
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {user_id} is not available"
        )
    user_profile = db.query(models.Profile).filter(models.Profile.user_id == user.id).first()
    return user_profile


def update_profile(user_id: int, request: schemas.UpdateProfile, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {user_id} is not available"
        )

    user_profile = db.query(models.Profile).filter(models.Profile.user_id == user_id).first()
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Profile with the user id {user_id} is not available"
        )

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")

    db.query(models.Profile).filter(user == user).delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
