from datetime import datetime, timedelta

from fastapi_jwt_auth import AuthJWT

from jose import JWTError, jwt
from pydantic import BaseModel

from . import schemas
from . import config

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES


# Generate Refresh Token Setting
# in production you can use Settings management
# from pydantic to get secret key from .env
class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY


# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()


# Generate Refresh Token Setting


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Use create_access_token() and create_refresh_token() to create our
    # access and refresh tokens
    # access_token = AuthJWT.create_access_token(subject=to_encode)
    # refresh_token = AuthJWT.create_refresh_token(subject=to_encode)
    # return {"access_token": access_token, "refresh_token": refresh_token}

    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.user.TokenData(username=username)
        return token_data
    except JWTError:
        raise credentials_exception
