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
    return country_id


@router.get("")
async def get_all_posts(country_id: int, db: Session = Depends(get_db)):
    pass


@router.get("/{post_id}")
async def get_post(country_id: int, post_id: int, db: Session = Depends(get_db)):
    pass


@router.put("/{post_id}")
async def put_post(country_id: int, post_id: int, db: Session = Depends(get_db)):
    pass


@router.delete("/{post_id}")
async def delete_post(country_id: int, post_id: int, db: Session = Depends(get_db)):
    pass


@router.post("/{post_id}/like")
async def like_post(country_id: int, post_id: int, db: Session = Depends(get_db)):
    pass


@router.post("/{post_id}/dislike")
async def dislike_post(country_id: int, post_id: int, db: Session = Depends(get_db)):
    pass
