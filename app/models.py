from typing import Optional

from pydantic import BaseModel

class User(BaseModel):
    username: str
    role: str
    organization: str
    level: int
    two_fa_secret: Optional[str] = None

class PolicyIn(BaseModel):
    sub: str
    obj: str
    act: str
    condition: str | None = None

class PolicyOut(PolicyIn):
    pass