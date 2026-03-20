from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.repository.auth_repo import auth_repo
from app.security.hash import verify_password , hash_password
from app.schemas.post_schema import UserLogin
from app.security.oauth2 import create_access_token

class AuthService:

    @staticmethod
    async def user_service(session: AsyncSession, user_credentials: OAuth2PasswordRequestForm):
        user_data = user_credentials
        user = await auth_repo.login_repo(session, user_data)
        if not user:
            raise HTTPException(status_code=403, detail="Invalid credentials")
        if not verify_password(user_credentials.password, user.password):
            raise HTTPException(status_code=403, detail="Invalid credentials")

        access_token = create_access_token(
            data={"user_id": str(user.id)}
        )
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

auth_service = AuthService()


