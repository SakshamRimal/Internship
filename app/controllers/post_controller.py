from fastapi import APIRouter, Depends
from app.core.db import SessionDep
from app.schemas.post_schema import PostSchemas
from app.service.post_service import get_all_post_service, create_post_service, get_post_by_id_service, \
    update_post_service, delete_post_service

router = APIRouter()

@router.get("/posts")
async def get_posts_controller(session: SessionDep):
    posts = await get_all_post_service(session)
    return {"data": posts}

@router.post("/posts")
async def create_post_controller(post: PostSchemas, session: SessionDep):
    new_post = await create_post_service(session , post)
    return {"data": new_post}

@router.get("/posts/{post_id}")
async def get_post_by_id_controller(post_id: int, session: SessionDep):
    post = await get_post_by_id_service(session, post_id)
    return {"data": post}

@router.put("/posts/{post_id}")
async def update_post_controller(post_id: int, post: PostSchemas, session: SessionDep ):
    updated_post = await update_post_service(session, post_id, post)
    return {"data": updated_post}

@router.delete("/posts/{post_id}")
async def delete_post_controller(post_id: int, session: SessionDep ):
    deleted = await delete_post_service(session, post_id)
    return {"data": deleted}