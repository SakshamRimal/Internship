from datetime import datetime

from sqlmodel import SQLModel, Field

# here we have class user tiers even if we remove the table name the table is created according to the class name
# since table = True so it will create the table based on table name so that it gives name to table
class UserTiers(SQLModel, table=True):
    __tablename__ = "user_tiers"

    tier_id: int | None = Field(default=None, primary_key=True)
    tier_name: str = Field(max_length=50)
    daily_limit: int = Field(default=0)
    transaction_fee: int = Field(default=0)


# this is to create the wallet which have the information about the balance etc
class Wallet(SQLModel, table=True):
    __tablename__ = "wallet"

    wallet_id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)
    total_balance: float = Field(default=0.0)


class User(SQLModel, table=True):
    __tablename__ = 'user'

    id: int | None = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(max_length=70, unique=True)
    number: int = Field(default=0 , max_length = 10)
    password: str = Field(max_length=150)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tier_id: int | None = Field(default=1, foreign_key="user_tiers.tier_id")