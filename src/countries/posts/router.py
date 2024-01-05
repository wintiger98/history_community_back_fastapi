from typing import List
from fastapi import APIRouter, HTTPException, Depends, Form, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...database import get_db
from ...auth.models import User
from ...auth.utils import get_current_user

router = APIRouter(
    prefix="/{country_id}/posts",
    tags=["posts"],
)


@router.post("")
async def post_posts(country_id: int, db: Session = Depends(get_db)):
    # 1. 국가 확인
    # 2. 게시글 생성
    return 


@router.get("")
async def get_all_posts(country_id: int, db: Session = Depends(get_db)):
    # 1. 국가 확인
    # 2. 게시글 조회
    pass


@router.get("/{post_id}")
async def get_post(country_id: int, post_id: int, db: Session = Depends(get_db)):
    # 1. 국가 확인
    # 2. 게시글 조회
    pass


@router.put("/{post_id}")
async def put_post(country_id: int, post_id: int, db: Session = Depends(get_db)):
    # 1. 국가 확인
    # 2. 게시글 조회
    # 3. 게시글 수정(작성자 여부 확인)
    pass


@router.delete("/{post_id}")
async def delete_post(country_id: int, post_id: int, db: Session = Depends(get_db)):
    # 1. 국가 확인
    # 2. 게시글 조회
    # 3. 게시글 삭제(작성자 여부 확인)
    pass


@router.post("/{post_id}/like")
async def like_post(country_id: int, post_id: int, db: Session = Depends(get_db)):
    # 1. 국가 확인
    # 2. 게시글 확인
    # 3. 좋아요
    pass


@router.post("/{post_id}/dislike")
async def dislike_post(country_id: int, post_id: int, db: Session = Depends(get_db)):
    # 1. 국가 확인
    # 2. 게시글 확인
    # 3. 싫어요
    pass
