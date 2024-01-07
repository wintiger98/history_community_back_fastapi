from fastapi import Depends, HTTPException, status
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from ...auth.models import User
from ..models import Country
from ..utils import get_countries

from .models import Post
from .schemas import PostInput


def make_post(data: PostInput, db: Session):
    new_post = Post(**data.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


def get_posts(filters: dict, db: Session):
    and_list = []
    for key, value in filters.items():
        and_list.append(getattr(Post, key) == value)

    stmt = select(Post).where(and_(*and_list))
    result = db.execute(stmt)
    posts = result.scalars().all()

    return posts


def update_post(data: PostInput, post: Post, db: Session):
    try:
        for key, value in data.model_dump().items():
            if value:
                setattr(post, key, value)
    except:
        return {"result": False, "detail": "post update failed"}
    try:
        db.commit()
    except:
        return {
            "result": False,
            "detail": "database commit failed while updating post",
        }
    return {"result": True}


def erase_post(post: Post, db: Session):
    try:
        db.delete(post)
        db.commit()

        return True
    except:
        return False
