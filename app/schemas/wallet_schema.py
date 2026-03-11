from pydantic import BaseModel


# this is what the user sees when they check their wallet balance
class WalletRead(BaseModel):
    wallet_id: int
    user_id: int
    total_balance: float

    class Config:
        from_attributes = True


# input: user sends this to deposit money into their wallet
class DepositRequest(BaseModel):
    user_id: int
    amount: float
