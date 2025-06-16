from datetime import datetime, timedelta, timezone
import jwt

from authx import AuthXConfig, AuthX
from app.core.config import auth_settings

auth_data = auth_settings.as_config_dict()
auth_data.pop("JWT_PRIVATE_KEY_PATH", None)
auth_data.pop("JWT_PUBLIC_KEY_PATH", None)

config = AuthXConfig(**auth_data)
auth = AuthX(config=config)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, auth_settings.JWT_SECRET_KEY, algorithm=auth_settings.JWT_ALGORITHM)
    return encoded_jwt

