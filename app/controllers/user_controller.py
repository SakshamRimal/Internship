from typing import List

from fastapi import APIRouter
from app.service.user_service import user_service
from app.core.db import SessionDep
from app.schemas.wallet_schema import UserResponse , UserBase
router = APIRouter(
    prefix="/user",
    tags=["users"],
)

@router.get("" ,response_model=List[UserResponse])
async def get_users(session: SessionDep):
    users = await user_service.get_user_service(session)
    return users

@router.post("" , response_model=UserResponse)
async def create_user(session: SessionDep , user_data: UserBase):
    users = await user_service.create_user_service(session , user_data)
    return users

@router.get("/{user_id}" , response_model=UserResponse)
async def get_user_by_id(session: SessionDep , user_id: int):
    user = await user_service.get_user_by_id(session , user_id)
    return user