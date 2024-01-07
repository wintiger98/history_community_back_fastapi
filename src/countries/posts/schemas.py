from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: int
    content: int


class PostInput(PostBase):
    pass


class PostOutput(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
