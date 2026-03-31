from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, text, String, Numeric, Enum, ForeignKey, Integer
from sqlmodel import Field, SQLModel
import enum


class UserTier(enum.Enum):
    BASIC = "basic"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=100, sa_column=Column(String(100), nullable=False, unique=True))
    password: str = Field(max_length=255, sa_column=Column(String(255), nullable=False))
    balance: float = Field(default=0.0, sa_column=Column(Numeric(10, 2), default=0.0))
    tier: UserTier = Field(default=UserTier.BASIC, sa_column=Column(Enum(UserTier), default=UserTier.BASIC))
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP")),
    )



class TransactionType(enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    TRANSFER = "transfer"
    PAYMENT = "payment"


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    type: TransactionType = Field(sa_column=Column(Enum(TransactionType), nullable=False))
    amount: float = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    description: Optional[str] = Field(default=None, max_length=500, sa_column=Column(String(500)))
    recipient_id: Optional[int] = Field(default=None, sa_column=Column(Integer, ForeignKey("users.id")))
    merchant: Optional[str] = Field(default=None, max_length=200, sa_column=Column(String(200)))
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP")),
    )