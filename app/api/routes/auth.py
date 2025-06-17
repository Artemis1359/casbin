from fastapi import APIRouter, Depends

from app.core.auth import get_current_user

router = APIRouter()

@router.post("/login")
async def login(user=Depends(get_current_user)):
    return {"msg": "Login endpoint"}

@router.post("/login2")
async def login():
    return {"msg": "Login endpoint"}
