from pydantic import BaseModel , Field
from typing import Annotated , Literal


class UserInput(BaseModel):
    transaction_description: Annotated[str, Field(..., description="Transaction description (e.g., Arby's Contactless)")]
    country: Annotated[Literal['australia', 'canada', 'india', 'uk', 'usa'], Field(description='Country of transaction')]
    currency: Annotated[Literal['aud', 'cad', 'gbp', 'inr', 'usd'], Field(description='Currency of transaction')]