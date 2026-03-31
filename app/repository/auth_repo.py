from fastapi import status , HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.schemas.wallet_schema import UserLogin
from app.models.wallet_model import User


class AuthRepo:

    @staticmethod
    async def login_repo(session: AsyncSession, user_credentials: OAuth2PasswordRequestForm) -> User:

        # it returns username and password no email
        statement = select(User).where(User.email == user_credentials.username)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()
        return user


auth_repo = AuthRepo()


