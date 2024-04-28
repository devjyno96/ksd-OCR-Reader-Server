from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from KsdNaverOCRServer import token_ocr

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_ocr.verify_token(data, credentials_exception)
