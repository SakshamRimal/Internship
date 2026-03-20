from typing import List, Dict
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.logger import logger
from app.repository.post_repo import post_repo
from app.schemas.post_schema import PostCreate
from app.models.post_model import Posts

class PostService:

    @staticmethod
    async def get_all_post_service(session: AsyncSession) -> List[Posts]:
        try:
            posts = await post_repo.get_post_repo(session)
            if not posts:
                logger.warning("Get All Posts: No records found in database")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No posts found"
                )

            logger.info(f"Get All Posts: Successfully fetched {len(posts)} posts")
            return posts

        except Exception:
            logger.exception("Get All Posts: Unexpected system error")
            raise

    @staticmethod
    async def create_post_service(session: AsyncSession, post: PostCreate) -> Posts:
        post_data = post.model_dump()
        try:
            created_post = await post_repo.create_post_repo(session, post_data)

            if not created_post:
                logger.error(f"Create Post: Repository failed to return object | data={post_data}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Post could not be created"
                )

            logger.info(f"Create Post: Success | id={created_post.id}")
            return created_post

        except Exception:
            logger.exception(f"Create Post: Critical error | data={post_data}")
            raise

    @staticmethod
    async def get_post_by_id_service(session: AsyncSession, post_id: int) -> Posts:
        try:
            post = await post_repo.get_post_by_id_repo(session, post_id)

            if post is None:
                logger.warning(f"Get Post By ID: Not found | id={post_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found"
                )

            logger.info(f"Get Post By ID: Success | id={post_id}")
            return post
        except Exception:
            logger.exception(f"Get Post By ID: System error | id={post_id}")
            raise

    @staticmethod
    async def update_post_service(session: AsyncSession, post_id: int, post: PostCreate) -> Posts:
        post_data = post.model_dump(exclude_unset=True)
        try:
            updated_post = await post_repo.update_post_repo(session, post_id, post_data)

            if not updated_post:
                logger.warning(f"Update Post: Target not found | id={post_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post with id {post_id} not found"
                )

            logger.info(f"Update Post: Success | id={post_id}")
            return updated_post

        except Exception:
            logger.exception(f"Update Post: System error | id={post_id}")
            raise

    @staticmethod
    async def delete_post_service(session: AsyncSession, post_id: int) -> Dict[str, str]:
        try:
            deleted = await post_repo.delete_post_repo(session, post_id)

            if not deleted:
                logger.warning(f"Delete Post: Target not found | id={post_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found"
                )

            logger.info(f"Delete Post: Success | id={post_id}")
            return {"detail": f"Post with id {post_id} deleted successfully"}

        except Exception:
            logger.exception(f"Delete Post: System error | id={post_id}")
            raise


post_service = PostService()