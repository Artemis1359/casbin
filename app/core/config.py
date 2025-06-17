import os
from datetime import timedelta
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()

casbin_model_conf = f'{PROJECT_ROOT}/model.conf'

env_model_conf = SettingsConfigDict(
        env_file=f'{PROJECT_ROOT}/.env',
        extra="ignore")

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    model_config = env_model_conf

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}")

class AuthXSettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "RS256"
    JWT_ENCODE_ISSUER: Optional[str]
    JWT_ACCESS_TOKEN_EXPIRES: Optional[timedelta] = timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES: Optional[timedelta] = timedelta(days=1)
    JWT_PRIVATE_KEY_PATH: Optional[str]
    JWT_PUBLIC_KEY_PATH: Optional[str]
    _private_key: Optional[str] = None
    _public_key: Optional[str] = None


    @property
    def JWT_PRIVATE_KEY(self) -> Optional[str]:
        if self._private_key is None and self.JWT_PRIVATE_KEY_PATH:
            path = PROJECT_ROOT / self.JWT_PRIVATE_KEY_PATH
            self._private_key = path.read_text()
        return self._private_key

    @property
    def JWT_PUBLIC_KEY(self) -> Optional[str]:
        if self._public_key is None and self.JWT_PUBLIC_KEY_PATH:
            path = PROJECT_ROOT / self.JWT_PUBLIC_KEY_PATH
            self._public_key = path.read_text()
        return self._public_key

    def as_config_dict(self):
        data = self.model_dump()
        data['JWT_PRIVATE_KEY'] = self.JWT_PRIVATE_KEY
        data['JWT_PUBLIC_KEY'] = self.JWT_PUBLIC_KEY
        data.pop("JWT_PRIVATE_KEY_PATH", None)
        data.pop("JWT_PUBLIC_KEY_PATH", None)
        return data

    model_config = env_model_conf

settings = Settings()
auth_settings = AuthXSettings()

# print(settings.get_db_url())
# print(auth_settings.as_config_dict())
# print(PROJECT_ROOT)

