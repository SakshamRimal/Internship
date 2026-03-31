from app.models.wallet_model import User, Transaction
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List


class UserRepo:

    @staticmethod
    async def get_all_users_repo(session: AsyncSession):
        statement = select(User)
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def create_user_repo(session: AsyncSession, user_data: dict):
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

    @staticmethod
    async def update_user_tier(session: AsyncSession, user: User, tier):
        user.tier = tier
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def update_user_balance(session: AsyncSession, user: User, amount: float):
        user.balance = float(user.balance) + amount
        await session.commit()
        await session.refresh(user)
        return user


user_repo = UserRepo()

