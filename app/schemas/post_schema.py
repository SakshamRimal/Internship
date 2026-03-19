from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[float] = None

class PostCreate(PostBase):
    pass

# for response schema
class PostResponse(PostBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = {
        "from_attributes": True
    }

