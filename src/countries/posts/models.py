from ...database import Base

from datetime import datetime
from sqlalchemy import (
    TEXT,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(TEXT)
    content = Column(TEXT)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="posts")

    country_id = Column(Integer, ForeignKey("country.id"))
    country = relationship("Country", back_populates="posts")

    like_dislikes = relationship("PostLikeDislike", back_populates="post")

    replies = relationship("Reply", back_populates="post")


class PostLikeDislike(Base):
    __tablename__ = "post_like_dislike"

    id = Column(Integer, primary_key=True, index=True)
    like = Column(Boolean, default=False)
    dislike = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="post_like_dislikes")

    post_id = Column(Integer, ForeignKey("post.id"))
    post = relationship("Post", back_populates="like_dislikes")
