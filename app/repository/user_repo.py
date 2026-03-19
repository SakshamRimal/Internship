from app.models.post_model import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

class UserRepo:

    @staticmethod
    async def get_user_repo(session: AsyncSession):
        statement = select(User)
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def create_user_repo(session: AsyncSession , user_data: dict):
        new_user = User(**user_data)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int):
        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)
        return result.scalars().first()

    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str):
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        return result.scalars().first()

user_repo = UserRepo()
