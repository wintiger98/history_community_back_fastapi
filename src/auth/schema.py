from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserInput(UserBase):
    password: str
    nickname: str


class UserOutput(UserBase):
    id: int
    nickname: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UserUpdate(BaseModel):
    password: Optional[str]
    nickname: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
