from fastapi import APIRouter

from app.core.database import SessionDep
from app.schemas.user_schemas import UserCreate, UserOut
from app.service.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut)
async def create_user_endpoint(user_data: UserCreate, session: SessionDep):
    return UserService.create_user(session, user_data)


@router.get("/{user_id}", response_model=UserOut)
async def get_user_endpoint(user_id: int, session: SessionDep):
    return UserService.get_user(session, user_id)