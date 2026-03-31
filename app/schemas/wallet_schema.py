from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, Union
from enum import Enum


class UserTier(str, Enum):
    BASIC = "basic"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"
    PAYMENT = "payment"


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    balance: float
    tier: UserTier
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class TierUpdate(BaseModel):
    tier: UserTier


class DepositRequest(BaseModel):
    amount: float


class WithdrawRequest(BaseModel):
    amount: float


class TransferRequest(BaseModel):
    recipient_email: EmailStr
    amount: float
    description: Optional[str] = None


class PaymentRequest(BaseModel):
    amount: float
    merchant: str
    description: Optional[str] = None


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    type: TransactionType
    amount: float
    description: Optional[Union[str, PaymentRequest]] = None
    recipient_id: Optional[int] = None
    merchant: Optional[str] = None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }