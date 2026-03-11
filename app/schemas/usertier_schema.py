from pydantic import BaseModel


class UserTierRead(BaseModel):
    tier_id: int
    tier_name: str
    daily_limit: int
    transaction_fee: int

    class Config:
        from_attributes = True