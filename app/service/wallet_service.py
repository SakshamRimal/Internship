from fastapi import HTTPException, status
from app.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.wallet_repo import user_repo, transaction_repo
from app.schemas.wallet_schema import UserCreate, TierUpdate, DepositRequest, WithdrawRequest, TransferRequest, PaymentRequest
from app.security.hash import hash_password
from app.models.wallet_model import TransactionType


class UserService:
    @staticmethod
    async def get_all_users_service(session: AsyncSession):
        try:
            users = await user_repo.get_all_users_repo(session)
            return users
        except Exception as e:
            logger.error("Error getting all users", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    @staticmethod
    async def create_user_service(session: AsyncSession, user_data: UserCreate):
        try:
            existing_user = await user_repo.get_user_by_email(session, user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
            hashed_password = hash_password(user_data.password)
            user_data_dict = user_data.model_dump()
            user_data_dict['password'] = hashed_password
            user = await user_repo.create_user_repo(session, user_data_dict)
            return user
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error creating user", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    @staticmethod
    async def get_user_by_id_service(session: AsyncSession, user_id: int):
        try:
            user = await user_repo.get_user_by_id(session, user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return user
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error getting user", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    @staticmethod
    async def update_user_tier_service(session: AsyncSession, user_id: int, tier_data: TierUpdate):
        try:
            user = await user_repo.get_user_by_id(session, user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            updated_user = await user_repo.update_user_tier(session, user, tier_data.tier)
            return updated_user
        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error updating user tier", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


user_service = UserService()


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