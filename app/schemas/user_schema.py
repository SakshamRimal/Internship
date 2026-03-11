from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    tier_id: int = 1


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    created_at: datetime
    tier_id: int | None = None

    class Config:
        from_attributes = True


class UserInLogin(BaseModel):
    email: EmailStr
    password: str


class UserWithToken(BaseModel):
    token: str