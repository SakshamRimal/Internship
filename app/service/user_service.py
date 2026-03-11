from app.repositories.user_repo import UserRepository
from app.repositories.usertier_repo import UserTierRepo
from app.repositories.wallet_repo import WalletRepository
from app.schemas.user_schema import UserOut, UserInLogin, UserWithToken, UserCreate
from app.secuirty.hashHelper import HashHelper
from app.secuirty.authHandler import AuthHandler
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

# from user repo we go to the service  session we have the business logic for all the operation like signup and login
# here we have to tie up with the user and tier and wallet first the process if signup where we have to keep the information about the tier and all
# then after tier and info is set based on that user can use the features

class UserService:

    def __init__(self, session: Session):
        self._userRepo = UserRepository(session=session)
        self._tierRepo = UserTierRepo(session=session)
        self._walletRepo = WalletRepository(session=session)

    # for signup with the user information and tier and etx we have to make a method for signup
    def signup(self, user_details: UserCreate) -> UserOut:

        # in repo, we have made the code for getting the email so if there is email already then return that the user is already registered to the user
        if self._userRepo.user_exist_by_email(email=user_details.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        # tier is set by and user when creating the user if there is no tier raise the excpetion
        tier = self._tierRepo.get_tier_by_id(tier_id=user_details.tier_id)
        if not tier:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Tier with id {user_details.tier_id} does not exist")

        hashed_password = HashHelper.get_password_hash(plain_password=user_details.password)
        user_details.password = hashed_password
        user = self._userRepo.create_user(user_data=user_details)
        self._walletRepo.create_wallet(user_id=user.id)
        return user

    # in this login we have created the auth handler and auth helper where it helps for authorization and authentication process
    def login(self, login_details: UserInLogin) -> UserWithToken:
        if not self._userRepo.user_exist_by_email(email=login_details.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not found")

        user = self._userRepo.get_user_by_email(email=login_details.email)
        if HashHelper.verify_password(plain_password=login_details.password, hashed_password=user.password):
            token = AuthHandler.sign_jwt(user_id=user.id)
            if token:
                return UserWithToken(token=token)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect Password")