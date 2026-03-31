from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.wallet_model import Transaction


class TransactionRepo:

    @staticmethod
    async def create_transaction_repo(session: AsyncSession, transaction_data: dict):
        new_transaction = Transaction(**transaction_data)
        session.add(new_transaction)
        await session.commit()
        await session.refresh(new_transaction)
        return new_transaction

    @staticmethod
    async def get_transactions_by_user(session: AsyncSession, user_id: int):
        statement = select(Transaction).where(Transaction.user_id == user_id).order_by(Transaction.created_at.desc())
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def get_transaction_by_id(session: AsyncSession, transaction_id: int):
        statement = select(Transaction).where(Transaction.id == transaction_id)
        result = await session.execute(statement)
        return result.scalars().first()


transaction_repo = TransactionRepo()