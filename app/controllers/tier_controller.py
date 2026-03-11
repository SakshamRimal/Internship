from fastapi import APIRouter
from app.schemas.usertier_schema import UserTierRead
from app.core.database import SessionDep
from app.service.usertier_service import UserTierService

tier_router = APIRouter()


# GET /tier — get all fixed tiers (Bronze, Silver, Gold)
@tier_router.get("/", response_model=list[UserTierRead])
async def get_all_tiers(session: SessionDep):
    return UserTierService(session=session).get_all_tiers()


# GET /tier/user/{user_id} — which tier does this user belong to
@tier_router.get("/user/{user_id}", response_model=UserTierRead)
async def get_user_tier(user_id: int, session: SessionDep):
    return UserTierService(session=session).get_user_tier(user_id=user_id)