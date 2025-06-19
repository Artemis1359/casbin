from typing import Annotated, Optional

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.api.db import Base

intpk=Annotated[int, mapped_column(primary_key=True)]

class Users(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    username: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    attrs: Mapped[Optional[dict[str]]] = mapped_column(JSONB)


class CasbinRule(Base):
    __tablename__ = "casbin_rule"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ptype: Mapped[str]

    v0: Mapped[str | None]
    v1: Mapped[str | None]
    v2: Mapped[str | None]
    v3: Mapped[str | None]
    v4: Mapped[str | None]
    v5: Mapped[str | None]

    def __str__(self):
        return ", ".join(filter(None, [self.ptype, self.v0, self.v1, self.v2, self.v3, self.v4, self.v5]))
