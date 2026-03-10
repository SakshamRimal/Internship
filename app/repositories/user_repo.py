from app.repositories.base import BaseRepository
from app.db.models.user import User
from app.schemas.user_schema import UserCreate

class UserRepository(BaseRepository):
    def create_user(self , user_data: UserCreate):
        # user create is the schema for creating the user
        # since we inherit the repository where there is session dependency
        # so we inherit it so we don't have to use it again and again

        newuser = User(**user_data.model_dump(exclude_none=True))
        # model dump we dump the data in database store it in database

        self.session.add(newuser)
        self.session.commit()
        self.session.refresh(newuser)

        return newuser

    def user_exist_by_email(self , email: str) -> bool:
        user = self.session.query(User).filter_by(email=email).first()
        return bool(user)

    def get_user_exist_by_email(self, email: str) -> User:
        user = self.session.query(User).filter_by(email=email).first()
        return user

    def get_user_by_id(self , user_id: int):
        user = self.session.query(User).filter_by(id=user_id).first()
        return user