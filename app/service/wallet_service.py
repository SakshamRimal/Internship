from fastapi import HTTPException, status
from app.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.transaction_repo import transaction_repo
from app.repository.wallet_repo import user_repo
from app.schemas.wallet_schema import UserCreate, TierUpdate, DepositRequest, WithdrawRequest, TransferRequest, PaymentRequest
from app.security.hash import hash_password
from app.models.wallet_model import TransactionType


class WalletService:
    @staticmethod
    async def deposit_service(session: AsyncSession, user_id: int, deposit_data: DepositRequest):
        try:
            user = await user_repo.get_user_by_id(session, user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            if deposit_data.amount <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be positive")

            await user_repo.update_user_balance(session, user, deposit_data.amount)

            transaction = await transaction_repo.create_transaction_repo(session, {
                "user_id": user_id,
                "type": TransactionType.DEPOSIT,
                "amount": deposit_data.amount,
                "description": f"Deposit of ${deposit_data.amount}"
            })

            return {"message": "Deposit successful", "new_balance": user.balance, "transaction": transaction}
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error during deposit", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    @staticmethod
    async def withdraw_service(session: AsyncSession, user_id: int, withdraw_data: WithdrawRequest):
        try:
            user = await user_repo.get_user_by_id(session, user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            if withdraw_data.amount <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be positive")

            if float(user.balance) < withdraw_data.amount:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")

            await user_repo.update_user_balance(session, user, -withdraw_data.amount)

            transaction = await transaction_repo.create_transaction_repo(session, {
                "user_id": user_id,
                "type": TransactionType.WITHDRAW,
                "amount": withdraw_data.amount,
                "description": f"Withdrawal of ${withdraw_data.amount}"
            })

            return {"message": "Withdrawal successful", "new_balance": user.balance, "transaction": transaction}
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error during withdrawal", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    @staticmethod
    async def transfer_service(session: AsyncSession, user_id: int, transfer_data: TransferRequest):
        try:
            sender = await user_repo.get_user_by_id(session, user_id)
            if not sender:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sender not found")

            recipient = await user_repo.get_user_by_email(session, transfer_data.recipient_email)
            if not recipient:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipient not found")

            if transfer_data.amount <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be positive")

            if float(sender.balance) < transfer_data.amount:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")

            await user_repo.update_user_balance(session, sender, -transfer_data.amount)
            await user_repo.update_user_balance(session, recipient, transfer_data.amount)

            transaction = await transaction_repo.create_transaction_repo(session, {
                "user_id": user_id,
                "type": TransactionType.TRANSFER,
                "amount": transfer_data.amount,
                "description": transfer_data.description or f"Transfer to {transfer_data.recipient_email}",
                "recipient_id": recipient.id
            })

            return {"message": "Transfer successful", "new_balance": sender.balance, "transaction": transaction}
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error during transfer", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    @staticmethod
    async def payment_service(session: AsyncSession, user_id: int, payment_data: PaymentRequest):
        try:
            user = await user_repo.get_user_by_id(session, user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            if payment_data.amount <= 0:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be positive")

            if float(user.balance) < payment_data.amount:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")

            await user_repo.update_user_balance(session, user, -payment_data.amount)

            transaction = await transaction_repo.create_transaction_repo(session, {
                "user_id": user_id,
                "type": TransactionType.PAYMENT,
                "amount": payment_data.amount,
                "description": payment_data.description or f"Payment to {payment_data.merchant}",
                "merchant": payment_data.merchant
            })

            return {"message": "Payment successful", "new_balance": user.balance, "transaction": transaction}
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error during payment", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


wallet_service = WalletService()
