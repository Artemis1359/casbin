
from fastapi import HTTPException, Response
from authx import AuthXConfig, AuthX
from fastapi.security import HTTPBearer

from app.api.db.queries import User
from app.api.models.auth import LoginRequest, RefreshRequest
from app.core.config import auth_settings

auth_data = auth_settings.as_config_dict()

config = AuthXConfig(**auth_data)
auth = AuthX(config=config)

security = HTTPBearer(auto_error=False)


async def auth_login(data: LoginRequest, response: Response):
    user = await User.select_user(data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    access_token = auth.create_access_token(
        uid=user["email"],
        data={"attrs": user["attrs"]},
        expires_in=600  # 10 мин
    )
    refresh_token = auth.create_refresh_token(uid=user["email"])
    auth.set_access_cookies(access_token, response)
    auth.set_refresh_cookies(refresh_token, response)

    return {"access_token": access_token, "refresh_token": refresh_token}


async def refresh(data: RefreshRequest):
    try:
        payload = auth.verify_token(data.refresh_token)
        email = payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = await User.select_user(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = auth.create_access_token(
        uid=user["email"],
        data={"attrs": user["attrs"]},
        expires_in=600
    )

    return {"access_token": new_access_token}
