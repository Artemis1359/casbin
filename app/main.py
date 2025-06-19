

from fastapi import FastAPI
from app.api.routes.policies import router as policy_router
from app.api.routes.auth import router as auth_router
from app.core.middleware import CasbinMiddleware




app = FastAPI(
    title="Prototype",
    description="Прототип Casbin с Istio в minikube",
    root_path="/v1",
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc"
)
app.include_router(policy_router)
app.include_router(auth_router, prefix="/auth")
app.add_middleware(CasbinMiddleware)

