from datetime import datetime
from ..database import Base
from ..mappers.models import user_country_mapper
from sqlalchemy import TEXT, Column, DateTime, Integer, func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    email = Column(TEXT, unique=True, nullable=False)
    password = Column(TEXT, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    nickname = Column(TEXT, nullable=False)

    countries = relationship(
        "Country", secondary=user_country_mapper, back_populates="users"
    )
    cheers = relationship("Cheer", back_populates="user")
    posts = relationship("Post", back_populates="user")
    replies = relationship("Reply", back_populates="user")
    post_like_dislikes = relationship("PostLikeDislike", back_populates="user")
    reply_like_dislikes = relationship("ReplyLikeDislike", back_populates="user")
