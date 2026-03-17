from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, text
from sqlmodel import Field, SQLModel

class Posts(SQLModel, table=True):
    __tablename__ = "posts"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=500)
    content: str = Field(max_length=500)
    published: bool = Field(default=True, sa_column=Column(Boolean, server_default=text("1")))
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, server_default=text("CURRENT_TIMESTAMP")),
    )
    rating: Optional[float] = Field(default=None, nullable=True)


