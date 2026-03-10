from sqlmodel import Session

from app.models.user_models import User
from app.repository.user_repository import UserRepository
from app.schemas.user_schemas import UserCreate


class UserService:

    @staticmethod
    def create_user(session: Session, user_data: UserCreate) -> User:
        return UserRepository.create_user(session, user_data)

    @staticmethod
    def get_user(session: Session, user_id: int) -> User:
        return UserRepository.get_user(session, user_id)