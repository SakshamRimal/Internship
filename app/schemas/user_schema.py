from pydantic import BaseModel , EmailStr
from typing import Optional

# this is required for all user it is required for sign up
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

# this is for response as we don't want to response password to the user
# so we have to make the user output response
# this is used for user login
class UserOutLogin(BaseModel):
    id: int
    email: EmailStr

# this is used for signup
class UserOut(UserOutLogin):
    first_name: str
    last_name: str

    # now we have to use config for response
    class Config:
        from_attributes = True

# this is for update if user wants to update any data then use
# schema based on this
class UserInUpdate(BaseModel):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

# this is for login we don't have to use all data for login
# only email and password is enough for login
class UserInLogin(BaseModel):
    email: EmailStr
    password: str

class UserWithToken(BaseModel):
    token: str


