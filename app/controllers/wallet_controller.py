from fastapi import APIRouter
from app.schemas.wallet_schema import WalletRead, DepositRequest
from app.core.database import SessionDep
from app.service.wallet_service import WalletService

wallet_router = APIRouter()


# POST /wallet/deposit — deposit money into wallet
@wallet_router.post("/deposit", response_model=WalletRead)
async def deposit(deposit_data: DepositRequest, session: SessionDep):
    return WalletService(session=session).deposit(deposit_data=deposit_data)


# GET /wallet/{user_id} — get wallet balance by user_id
@wallet_router.get("/{user_id}", response_model=WalletRead)
async def get_wallet(user_id: int, session: SessionDep):
    return WalletService(session=session).get_wallet_by_user_id(user_id=user_id)