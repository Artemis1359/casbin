from contextlib import asynccontextmanager


from fastapi import FastAPI
from app.api.routes.policies import router as policy_router
from app.api.routes.auth import router as auth_router
from app.core.casbin import create_enforcer


@asynccontextmanager
async def lifespan(app: FastAPI):

    enforcer = await create_enforcer()
    app.state.enforcer = enforcer
    yield

app = FastAPI(
    title="Prototype",
    description="Прототип Casbin с Istio в minikube",
    root_path="/v1",
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
    lifespan=lifespan
)
app.include_router(policy_router)
app.include_router(auth_router, prefix="/auth")

