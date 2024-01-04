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
async def detst(country_id: int, db: Session = Depends(get_db)):
    return country_id
