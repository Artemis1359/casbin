from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from app.core.casbin import EnforcerSingleton


class CasbinMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        enforcer = await EnforcerSingleton.get_instance()
        role = request.headers.get("X-User", "anonymous")
        sub = {'role': role}
        obj = request.url.path
        act = request.method.lower()

        allowed =  enforcer.enforce(sub, obj, act)
        if not allowed:
            return JSONResponse(status_code=403, content={"detail": "Forbidden"})

        response = await call_next(request)
        return response
