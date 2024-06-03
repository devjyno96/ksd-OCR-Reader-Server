from fastapi.requests import Request
from jose import jwt
from sqladmin.authentication import AuthenticationBackend

from app.config import settings

# TODO : 실재 유저 로그인과 연결해야합니다 임시로 하드코딩 되어있음


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        if username == "admin" and password == settings.PASSWORD:
            encoded_jwt = jwt.encode(
                {"username": username, "password": settings.PASSWORD},
                settings.SECRET_KEY,
                algorithm=settings.ALGORITHM,
            )
            request.session.update({"token": encoded_jwt})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        decrypted_value = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username, password = decrypted_value["username"], decrypted_value["password"]

        if username == "admin" and password == settings.PASSWORD:
            return True

        return False


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)