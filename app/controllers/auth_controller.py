from fastapi import APIRouter
from app.schemas.user_schema import UserInLogin, UserCreate, UserOut, UserWithToken
from app.core.database import SessionDep
from app.service.user_service import UserService

auth_router = APIRouter()


@auth_router.post("/signup", response_model=UserOut)
async def signup(usersignup: UserCreate, session: SessionDep):
    return UserService(session=session).signup(user_details=usersignup)


@auth_router.post("/login", response_model=UserWithToken)
async def login(userlogin: UserInLogin, session: SessionDep):
    return UserService(session=session).login(login_details=userlogin)