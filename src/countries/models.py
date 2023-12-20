from datetime import datetime
from ..database import Base
from sqlalchemy import TEXT, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..mappers.models import user_country_mapper


class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(20), unique=True)

    users = relationship(
        "User", secondary=user_country_mapper, back_populates="countries"
    )
    posts = relationship("Post", back_populates="country")
    cheers = relationship("Cheer", back_populates="country")


class Cheer(Base):
    __tablename__ = "cheers"

    id = Column(Integer, primary_key=True, index=True, unique=True)

    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="cheers")

    country_id = Column(Integer, ForeignKey("country.id"))
    country = relationship("Country", back_populates="cheers")
