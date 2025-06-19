from authx import RequestToken
from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str

class RefreshRequest(BaseModel):
    refresh_token: RequestToken
