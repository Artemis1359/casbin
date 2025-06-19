import asyncio

from app.api.db import Base, engine, async_session
from app.api.db.models import Users, CasbinRule
from app.core.casbin import create_enforcer


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def input_users():
    async with async_session() as session:
        user1 = Users(
            id=1,
            username='admin',
            email='admin@admin.ru',
            attrs={'role': 'admin'}
        )
        session.add(user1)
        await session.commit()

async def input_casbin_rule():
    async with async_session() as session:
        rule1 = CasbinRule(
            id=1,
            ptype='p',
            v0='/auth/hello',
            v1='get',
            v2='sub.role=="admin"'
        )
        rule2 = CasbinRule(
            id=2,
            ptype='p',
            v0='/auth/login',
            v1='post',
            v2='sub.role=="anonymous"'
        )
        session.add_all([rule1, rule2])
        await session.commit()

async def creation():
    await create_tables()
    await input_users()
    await input_casbin_rule()
    enforcer = await create_enforcer()
    await enforcer.load_policy()

asyncio.run(creation())