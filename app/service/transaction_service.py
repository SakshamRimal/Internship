from fastapi import HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import logger
from app.repository.transaction_repo import transaction_repo

class TransactionService:
    @staticmethod
    async def get_transaction_history_service(session: AsyncSession, user_id: int):
        try:
            transactions = await transaction_repo.get_transactions_by_user(session, user_id)
            return transactions
        except Exception as e:
            logger.error("Error getting transaction history", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    @staticmethod
    async def get_transaction_by_id_service(session: AsyncSession, transaction_id: int):
        try:
            transaction = await transaction_repo.get_transaction_by_id(session, transaction_id)
            if not transaction:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
            return transaction
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error getting transaction", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


transaction_service = TransactionService()