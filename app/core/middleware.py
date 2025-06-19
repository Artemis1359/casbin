from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from app.core.auth import auth
from app.core.casbin import EnforcerSingleton
from app.core.logger_config import logger


class CasbinMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):

        role = 'anonymous'
        try:
            token = await auth.get_access_token_from_request(request)
            logger.info(token)
            if token:
                payload = auth.verify_token(token)
                logger.info(payload)
                role = payload.attrs.get('role', 'anonymous')

            logger.info(f'role --- {role}')
        except Exception as e:
            logger.error(e)

        request.state.user = {"role": role}


        sub = {'role': role}
        obj = request.url.path
        act = request.method.lower()
        enforcer = await EnforcerSingleton.get_instance()
        allowed = enforcer.enforce(sub, obj, act)
        if not allowed:
            return JSONResponse(status_code=403, content={"detail": "Forbidden CASBIN"})

        response = await call_next(request)
        return response
