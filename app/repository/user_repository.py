from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.models.user_models import User
from app.schemas.user_schemas import UserCreate


class UserRepository:

    @staticmethod
    def create_user(session: Session, user_data: UserCreate) -> User:
        user = User(**user_data.model_dump())
        session.add(user)
        try:
            session.commit()
            session.refresh(user)
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=400, detail="User already exists")
        return user

    @staticmethod
    def get_user(session: Session, user_id: int) -> User:
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user