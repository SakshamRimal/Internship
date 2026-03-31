from typing import List
from fastapi import APIRouter, status, Depends
from app.security.oauth2 import get_current_user
from app.service.user_service import user_service
from app.core.db import SessionDep
from app.schemas.wallet_schema import UserResponse, UserBase, UserCreate, TierUpdate

router = APIRouter(
    prefix="/user",
    tags=["users"],
)

@router.get("", response_model=List[UserResponse])
async def get_users(session: SessionDep):
    users = await user_service.get_user_service(session)
    return users


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(session: SessionDep, user_data: UserCreate):
    user = await user_service.create_user_service(session, user_data)
    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_data(
    session: SessionDep,
    current_user: int = Depends(get_current_user)
):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(session: SessionDep, user_id: int):
    user = await user_service.get_user_by_id(session, user_id)
    return user


@router.put("/{user_id}/tier", response_model=UserResponse)
async def update_user_tier(
    user_id: int,
    tier_data: TierUpdate,
    session: SessionDep,
    current_user: int = Depends(get_current_user)
):
    user = await user_service.update_user_tier_service(session, user_id, tier_data)
    return user
