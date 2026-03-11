from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.wallet_repo import WalletRepository
from app.schemas.wallet_schema import WalletRead, DepositRequest


class WalletService:

    def __init__(self, session: Session):
        self._walletRepo = WalletRepository(session=session)

    # get wallet by user_id
    def get_wallet_by_user_id(self, user_id: int) -> WalletRead:
        wallet = self._walletRepo.get_wallet_by_user_id(user_id=user_id)
        if not wallet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Wallet not found for user {user_id}")
        return wallet

    # deposit money into the user's wallet
    # validates amount > 0 and wallet exists, then adds the amount to total_balance
    def deposit(self, deposit_data: DepositRequest) -> WalletRead:
        if deposit_data.amount <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be greater than 0")

        wallet = self._walletRepo.get_wallet_by_user_id(user_id=deposit_data.user_id)
        if not wallet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Wallet not found for user {deposit_data.user_id}")

        # add the amount to wallet and return updated wallet
        updated_wallet = self._walletRepo.deposit_balance(user_id=deposit_data.user_id, amount=deposit_data.amount)
        return updated_wallet



