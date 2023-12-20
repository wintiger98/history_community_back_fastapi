from ....database import Base

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


class Reply(Base):
    __tablename__ = "reply"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    content = Column(TEXT)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="replies")

    post_id = Column(Integer, ForeignKey("post.id"))
    post = relationship("Post", back_populates="replies")

    like_dislikes = relationship("ReplyLikeDislike", back_populates="reply")


class ReplyLikeDislike(Base):
    __tablename__ = "reply_like_dislikes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    reply_id = Column(Integer, ForeignKey("reply.id"))
    like = Column(Boolean, default=False)
    dislike = Column(Boolean, default=False)

    user = relationship("User", back_populates="reply_like_dislikes")
    reply = relationship("Reply", back_populates="like_dislikes")
