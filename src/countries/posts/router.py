from typing import List
from fastapi import APIRouter, HTTPException, Depends, Form, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...database import get_db
from ...auth.models import User
from ...auth.utils import get_current_user

from ..utils import get_country_by_id

from .utils import make_post, get_posts, update_post, erase_post
from .schemas import PostInput, PostOutput

router = APIRouter(
    prefix="/{country_id}/posts",
    tags=["posts"],
)


@router.post("", response_model=PostOutput)
async def post_post(country_id: int, data: PostInput, db: Session = Depends(get_db)):
    # 1. 국가 확인
    country = get_country_by_id(country_id=country_id, db=db)
    # 2. 게시글 생성
    post = make_post(data=data, db=db)

    return post


@router.get("")
async def get_all_posts(country_id: int, db: Session = Depends(get_db)):
    # 1. 국가 확인
    country = get_country_by_id(country_id=country_id, db=db)
    # 2. 게시글 조회
    filters = {"country_id": country.id}
    posts = get_posts(filters=filters, db=db)
    return posts


@router.get("/{post_id}")
async def get_post(country_id: int, post_id: int, db: Session = Depends(get_db)):
    # 1. 국가 확인
    country = get_country_by_id(country_id=country_id, db=db)
    # 2. 게시글 조회
    filters = {"id": post_id}
    post = get_posts(filters=filters, db=db)
    return post[0]


@router.put("/{post_id}")
async def put_post(
    country_id: int, post_id: int, data: PostInput, db: Session = Depends(get_db)
):
    # 1. 국가 확인
    country = get_country_by_id(country_id=country_id, db=db)
    # 2. 게시글 조회
    filters = {"id": post_id}
    post = get_posts(filters=filters, db=db)
    post = post[0]
    # 3. 게시글 수정(작성자 여부 확인)
    post = update_post(data=data, post=post, db=db)
    pass


@router.delete("/{post_id}")
async def delete_post(country_id: int, post_id: int, db: Session = Depends(get_db)):
    # 1. 국가 확인
    country = get_country_by_id(country_id=country_id, db=db)
    # 2. 게시글 조회
    filters = {"id": post_id}
    post = get_posts(filters=filters, db=db)
    post = post[0]
    # 3. 게시글 삭제(작성자 여부 확인)
    result = erase_post(post=post, db=db)
    if not result:
        raise HTTPException(400, detail="Delete failed")
    else:
        return {"result": True, "detail": "Delete success"}


@router.post("/{post_id}/like")
async def like_post(country_id: int, post_id: int, db: Session = Depends(get_db)):
    # 1. 국가 확인
    country = get_country_by_id(country_id=country_id, db=db)
    # 2. 게시글 확인
    filters = {"id": post_id}
    post = get_posts(filters=filters, db=db)
    post = post[0]
    # 3. 좋아요
    pass


@router.post("/{post_id}/dislike")
async def dislike_post(country_id: int, post_id: int, db: Session = Depends(get_db)):
    # 1. 국가 확인
    country = get_country_by_id(country_id=country_id, db=db)
    # 2. 게시글 확인
    filters = {"id": post_id}
    post = get_posts(filters=filters, db=db)
    post = post[0]
    # 3. 싫어요
    pass
