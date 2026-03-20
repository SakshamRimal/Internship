from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.db import SessionDep
from app.schemas.post_schema import PostCreate , PostResponse
from app.security import oauth2
from app.service.post_service import post_service

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)

@router.get("" , response_model=List[PostResponse])
async def get_posts_controller(session: SessionDep):
    posts = await post_service.get_all_post_service(session)
    return posts

@router.post("" , status_code=status.HTTP_201_CREATED , response_model=PostResponse)
async def create_post_controller(post: PostCreate, session: SessionDep , current_user: int = Depends(oauth2.get_current_user)):
    new_post = await post_service.create_post_service(session, post)
    return new_post

@router.get("/{post_id}" , response_model=PostResponse)
async def get_post_by_id_controller(post_id: int, session: SessionDep , current_user : int = Depends(oauth2.get_current_user)):
    post = await post_service.get_post_by_id_service(session, post_id)
    return post

@router.put("/{post_id}" , response_model=PostResponse)
async def update_post_controller(post_id: int, post: PostCreate, session: SessionDep , current_user : int = Depends(oauth2.get_current_user)):
    updated_post = await post_service.update_post_service(session, post_id, post)
    return updated_post

@router.delete("/{post_id}")
async def delete_post_controller(post_id: int, session: SessionDep , current_user : int = Depends(oauth2.get_current_user)):
    deleted = await post_service.delete_post_service(session, post_id)
    return deleted

