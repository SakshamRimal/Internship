from fastapi import APIRouter, Depends
from app.service.wallet_service import wallet_service
from app.core.db import SessionDep
from app.schemas.wallet_schema import (
    DepositRequest, WithdrawRequest, TransferRequest, PaymentRequest,
)
from app.security.oauth2 import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["users"],
)
@router.post("/deposit", response_model=dict)
async def deposit(
    deposit_data: DepositRequest,
    session: SessionDep,
    current_user: int = Depends(get_current_user)
):
    result = await wallet_service.deposit_service(session, current_user.id, deposit_data)
    return result


@router.post("/withdraw", response_model=dict)
async def withdraw(
    withdraw_data: WithdrawRequest,
    session: SessionDep,
    current_user: int = Depends(get_current_user)
):
    result = await wallet_service.withdraw_service(session, current_user.id, withdraw_data)
    return result


@router.post("/transfer", response_model=dict)
async def transfer(
    transfer_data: TransferRequest,
    session: SessionDep,
    current_user: int = Depends(get_current_user)
):
    result = await wallet_service.transfer_service(session, current_user.id, transfer_data)
    return result


@router.post("/payment", response_model=dict)
async def payment(
    payment_data: PaymentRequest,
    session: SessionDep,
    current_user: int = Depends(get_current_user)
):
    result = await wallet_service.payment_service(session, current_user.id, payment_data)
    return result


