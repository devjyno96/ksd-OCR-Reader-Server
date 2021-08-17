import enum
from typing import List, Optional

from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    is_admin: Optional[bool] = False


class ShowUser(BaseModel):
    username: str
    first_name: str
    last_name: str
    is_admin: bool

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class ChangePassword(BaseModel):
    username: str
    new_password: str
    check_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class ShowUserWithID(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    is_admin: Optional[str]

    class Config():
        orm_mode = True


class Profile(BaseModel):
    email: Optional[str]

    class Config():
        orm_mode = True

class CreateProfile(Profile):
    user_id:int

class UpdateProfile(Profile):
    pass