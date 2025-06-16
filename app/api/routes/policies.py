from casbin import AsyncEnforcer
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.casbin import add_policy, remove_policy
from app.core.casbin import get_enforcer
from app.models import PolicyIn, PolicyOut

router = APIRouter()






@router.post("/policies", response_model=PolicyOut, status_code=status.HTTP_201_CREATED)
async def create_policy(policy: PolicyIn, enforcer: AsyncEnforcer = Depends(get_enforcer)):
    added = await add_policy(enforcer, policy.sub, policy.obj, policy.act, policy.condition or "")
    if not added:
        raise HTTPException(status_code=400, detail="Policy already exists or could not be added")
    await enforcer.save_policy()
    return policy


@router.delete("/policies", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(policy: PolicyIn, enforcer: AsyncEnforcer = Depends(get_enforcer)):
    removed = await remove_policy(enforcer, policy.sub, policy.obj, policy.act, policy.condition or "")
    if not removed:
        raise HTTPException(status_code=404, detail="Policy not found")
    await enforcer.save_policy()
    return None


@router.get("/policies", response_model=list[PolicyOut])
async def list_policies(enforcer: AsyncEnforcer = Depends(get_enforcer)):
    policies = await enforcer.get_policy()
    return [PolicyOut(sub=p[0], obj=p[1], act=p[2], condition=p[3] if len(p) > 3 else "") for p in policies]