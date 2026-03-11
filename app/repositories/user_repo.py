from app.repositories.base import BaseRepository
from app.db.models.user import User
from app.schemas.user_schema import UserCreate


class UserRepository(BaseRepository):

    # here we inherited the base repo because it has session that we need to interact with the database
    # we have to create the user and keep it into the database
    def create_user(self, user_data: UserCreate):

        # we extract the data by using model_dump from the database and none will be excluded in this case
        newuser = User(**user_data.model_dump(exclude_none=True))

        # in session, we add new user add the information of the user to the session, and it will add it to the database
        self.session.add(newuser)

        # after adding the session we have to commit it to the database to save the changes
        self.session.commit()

        # and refresh the database by passing into the new user
        self.session.refresh(newuser)
        return newuser

    def user_exist_by_email(self, email: str) -> bool:

        # use session and query and extract the information by using email and extract the first row it extract only one row that we need
        user = self.session.query(User).filter_by(email=email).first()
        return user is not None

    def get_user_by_email(self, email: str) -> User:
        user = self.session.query(User).filter_by(email=email).first()
        return user

    def get_user_by_id(self, user_id: int) -> User:
        user = self.session.query(User).filter_by(id=user_id).first()
        return user