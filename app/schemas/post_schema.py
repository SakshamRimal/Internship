from pydantic import BaseModel
from typing import Optional
import datetime

# ------- this is pydantic schemas for validation -------------------------------------------
class PostSchemas(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at: Optional[datetime.datetime] = None
    rating: Optional[float] = None

