from fastapi import status, Depends
from app.service.auth_service import auth_service
from fastapi import APIRouter
from app.core.db import SessionDep
from app.schemas.post_schema import UserLogin, PostResponse , Token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["auth"]
)

@router.post("/login", status_code=status.HTTP_200_OK ,response_model=Token)
async def login(session: SessionDep , user_credentials: OAuth2PasswordRequestForm = Depends()):
    users = await auth_service.user_service(session , user_credentials)
    return users

