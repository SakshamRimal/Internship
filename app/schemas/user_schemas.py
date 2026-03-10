from pydantic import EmailStr, BaseModel


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


# user response
class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
