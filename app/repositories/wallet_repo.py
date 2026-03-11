from app.repositories.base import BaseRepository
from app.db.models.user import Wallet


class WalletRepository(BaseRepository):

    # create a new wallet for a user with 0 balance
    def create_wallet(self, user_id: int) -> Wallet:
        wallet = Wallet(user_id=user_id, total_balance=0.0)
        self.session.add(wallet)
        self.session.commit()
        self.session.refresh(wallet)
        return wallet

    # get wallet by user_id
    def get_wallet_by_user_id(self, user_id: int) -> Wallet | None:
        wallet = self.session.query(Wallet).filter_by(user_id=user_id).first()
        return wallet

    # add money to a user's wallet
    def deposit_balance(self, user_id: int, amount: float) -> Wallet:
        wallet = self.session.query(Wallet).filter_by(user_id=user_id).first()
        wallet.total_balance += amount
        self.session.commit()
        self.session.refresh(wallet)
        return wallet

    def transfer_amount(self , user_id: int, amount: float) -> Wallet:
        wallet = self.session.query(Wallet).filter_by(user_id=user_id).first()
        wallet.total_balance -= amount
        self.session.commit()
        self.session.refresh(wallet)
        return wallet