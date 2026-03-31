from typing import List

from fastapi import APIRouter, Depends

from app.core.db import SessionDep
from app.schemas.wallet_schema import TransactionResponse
from app.security.oauth2 import get_current_user
from app.service.transaction_service import transaction_service

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)

@router.get("", response_model=List[TransactionResponse])
async def get_transaction_history(
    session: SessionDep,
    current_user: int = Depends(get_current_user)
):
    transactions = await transaction_service.get_transaction_history_service(session, current_user.id)
    return transactions


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    session: SessionDep,
    current_user: int = Depends(get_current_user)
):
    transaction = await transaction_service.get_transaction_by_id_service(session, transaction_id)
    return transaction