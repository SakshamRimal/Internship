from fastapi import HTTPException , status
from app.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.user_repo import user_repo
from app.schemas.post_schema import UserBase
from app.security.hash import hash_password

class UserService:
    @staticmethod
    async def get_user_service(session: AsyncSession):
        try:
            users =await user_repo.get_user_repo(session)
            if users is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return users
        except Exception as e:
            logger.error(f"Error getting all posts: {e}")
            raise

    @staticmethod
    async def create_user_service(session: AsyncSession , users_data: UserBase):
        try:
            # for checking if the email already exist or not we write this code
            existing_user = await user_repo.get_user_by_email(session, users_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists"
                )
            # hash the password
            hashed_password = hash_password(users_data.password)
            users_data.password = hashed_password

            user_data = users_data.model_dump()
            users = await  user_repo.create_user_repo(session , user_data)

            if users is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Invalid data")
            return users
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int):
        try:
            users = await user_repo.get_user_by_id(session , user_id)
            if users is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return users
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            raise


user_service = UserService()