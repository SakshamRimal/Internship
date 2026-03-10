import datetime as dt
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    password: str = Field(max_length=255, index=True)
    is_active: bool = Field(default=True)
    date_joined: dt.datetime = Field(default_factory=dt.datetime.now)