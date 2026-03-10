from app.repositories.user_repo import UserRepository
from app.schemas.user_schema import UserOut , UserInLogin , UserWithToken , UserCreate
from app.secuirty.hashHelper import HashHelper
from app.secuirty.authHandler import AuthHandler
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

class UserService:
    def __init__(self , session : Session):
        self._userRepository = UserRepository(session= session)

    def signup(self , user_details: UserCreate) -> UserOut:
        if self._userRepository.user_exist_by_email(email=user_details.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Email already registered")

        hashed_password = HashHelper.get_password_hash(plain_password= user_details.password)
        user_details.password = hashed_password
        return self._userRepository.create_user(user_data= user_details)

    def login(self , login_details: UserInLogin) -> UserWithToken:
        if not self._userRepository.user_exist_by_email(email=login_details.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Email not found")

        user = self._userRepository.get_user_exist_by_email(email=login_details.email)
        if HashHelper.verify_password(plain_password= login_details.password, hashed_password= user.password):
            token = AuthHandler.sign_jwt(user_id=user.id)
            if token:
                return UserWithToken(token=token)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Incorrect Password")