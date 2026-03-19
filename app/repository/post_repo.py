from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post_model import Posts

class PostRepo:

    @staticmethod
    async def get_post_repo(session: AsyncSession):
        statement = select(Posts)
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def create_post_repo(session: AsyncSession, post_data: dict):
        new_post = Posts(**post_data)  # just use dict directly
        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)
        return new_post

    @staticmethod
    async def get_post_by_id_repo(session: AsyncSession, id: int):
        return await session.get(Posts, id)

    @staticmethod
    async def update_post_repo(session: AsyncSession, id: int, post_data: dict):
        db_post = await session.get(Posts, id)
        if not db_post:
            return None
        # update only provided fields
        for key, value in post_data.items():
            setattr(db_post, key, value)
        session.add(db_post)
        await session.commit()
        await session.refresh(db_post)
        return db_post

    @staticmethod
    async def delete_post_repo(session: AsyncSession, id: int):
        db_post = await session.get(Posts, id)
        if not db_post:
            return False
        await session.delete(db_post)
        await session.commit()
        return True

post_repo = PostRepo()