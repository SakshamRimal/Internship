from typing import List
from fastapi import APIRouter, Depends, status
from app.service.wallet_service import user_service, wallet_service, transaction_service
from app.service.auth_service import auth_service
from app.core.db import SessionDep
from app.schemas.wallet_schema import (
    UserResponse, UserCreate, TierUpdate,
    DepositRequest, WithdrawRequest, TransferRequest, PaymentRequest,
    TransactionResponse, Token
)
from app.security.oauth2 import create_access_token, verify_access_token, get_current_user
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/user",
    tags=["users"],
)


@router.get("", response_model=List[UserResponse])
async def get_users(session: SessionDep):
    users = await user_service.get_all_users_service(session)
    return users


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(session: SessionDep, user_data: UserCreate):
    user = await user_service.create_user_service(session, user_data)
    return user


@router.get("/me", response_model=UserResponse)
async def get_current_user_data(
    session: SessionDep,
    current_user: int = Depends(get_current_user)
):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(session: SessionDep, user_id: int):
    user = await user_service.get_user_by_id_service(session, user_id)
    return user


@router.put("/{user_id}/tier", response_model=UserResponse)
async def update_user_tier(
    user_id: int,
    tier_data: TierUpdate,
    session: SessionDep,
    current_user: int = Depends(get_current_user)
):
    user = await user_service.update_user_tier_service(session, user_id, tier_data)
    return user


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


@router.get("/transactions", response_model=List[TransactionResponse])
async def get_transaction_history(
    session: SessionDep,
    current_user: int = Depends(get_current_user)
):
    transactions = await transaction_service.get_transaction_history_service(session, current_user.id)
    return transactions


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    session: SessionDep,
    current_user: int = Depends(get_current_user)
):
    transaction = await transaction_service.get_transaction_by_id_service(session, transaction_id)
    return transaction