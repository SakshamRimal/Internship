from fastapi import APIRouter

from app.core.database import SessionDep
from app.schemas.user_schemas import UserCreate, UserOut
from app.service.user_service import UserService

authRouter = APIRouter(tags=["Auth"])


@authRouter.post("/login")
def login(login_data: UserCreate):
    return {"data": "login"}


@authRouter.post("/signup", response_model=UserOut)
def signup(signup_data: UserCreate, session: SessionDep):
    return UserService.create_user(session, signup_data)