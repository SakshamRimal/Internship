# authorization and authentication
from fastapi import APIRouter, HTTPException
from starlette import status
from app.schemas.user_schema import UserInLogin , UserCreate , UserOut , UserWithToken
from app.core.database import SessionDep
from app.service.user_service import UserService

auth_router = APIRouter()

@auth_router.post("/signup" , response_model=UserOut)
async def signup(usersignup: UserCreate , session: SessionDep):
    try:
        user = UserService(session = session).signup(user_details=usersignup)
        return user
    except Exception as err:
        print(err)
        raise err

@auth_router.post("/login" , response_model=UserWithToken)
async def login(userlogin: UserInLogin , session: SessionDep):
    try:
        user = UserService(session = session).login(login_details=userlogin)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Incorrect username or password")
    return user

# router -> service -> repository -> db
#router <- service <- repository <- db