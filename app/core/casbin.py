from simpleeval import SimpleEval
from typing import Dict, Any
from fastapi import Request
from casbin_async_sqlalchemy_adapter.adapter import Adapter
from app.core.config import casbin_model_conf, settings
import casbin

from app.core.logger_config import logger


class EnforcerSingleton:
    _instance = None

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            cls._instance = await create_enforcer()
        return cls._instance


async def create_enforcer():
    adapter = Adapter(settings.get_db_url())
    await adapter.create_table()  # создаём таблицы, если их нет

    model = casbin.Model()
    model.load_model(casbin_model_conf)

    enforcer = casbin.AsyncEnforcer(model, adapter, enable_log=False)
    enforcer.add_function("eval_rule", eval_rule)
    await enforcer.load_policy()
    return enforcer

async def get_enforcer(request: Request):
    return await EnforcerSingleton.get_instance()

def eval_rule(sub: Dict[str, Any], obj: str, act: str, condition: str) -> bool:
    if not condition or not condition.strip():
        return False
    s = SimpleEval(
        names={
            "sub": sub,
            "obj": obj,
            "act": act,
        }
    )
    logger.info(f'{condition} ----- {s.eval(condition)}')
    try:
        return s.eval(condition)
    except Exception as e:
        logger.error(f"Eval error: {e}")
        return False



async def add_policy(enforcer, sub, obj, act, condition):
    return await enforcer.add_policy(sub, obj, act, condition)

async def remove_policy(enforcer, sub, obj, act, condition):
    return await enforcer.remove_policy(sub, obj, act, condition)
