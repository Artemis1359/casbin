from fastapi import APIRouter, Depends, Response

from app.api.models.auth import LoginRequest
from app.core.auth import auth, auth_login

router = APIRouter()

@router.post("/login")
async def login(data: LoginRequest, response: Response):
    """Вход в систему."""

    return await auth_login(data, response)

# Если оставляем проверку на все роуты через Casbin,
# то работаем через policies, Depends не нужны
# @router.get("/hello")
# async def hello(user = Depends(auth.access_token_required)):
#     return {"msg": f"Hello, {user}!"}


@router.get("/hello")
async def hello():
    return {"msg": f"Hello!"}