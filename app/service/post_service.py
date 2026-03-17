from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repository.post_repo import get_post_repo, create_post_repo, get_post_by_id_repo, update_post_repo, delete_post_repo
from app.schemas.post_schema import PostSchemas

# use session from orm in repo and service only use the session dependency in routing in our main

async def get_all_post_service(session: Session):
    posts = await get_post_repo(session)
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return posts

async def create_post_service(session: Session , post: PostSchemas):
    new_post = PostSchemas(**post.model_dump())
    created_post = await create_post_repo(session , new_post)
    if not created_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not created")
    return created_post

async def get_post_by_id_service(session: Session  ,post_id: int):
    post = await get_post_by_id_repo(session , post_id )
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


async def update_post_service(session: Session, post_id: int, post_schema: PostSchemas):
    # Pass the data to the repo and let the repo return the updated object
    updated_post = await update_post_repo(session, post_id, post_schema)
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    return updated_post

async def delete_post_service(session: Session , post_id: int):
    row_count = await delete_post_repo(session , post_id)
    if row_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"deleted": f"Post with id:{post_id} deleted"}

