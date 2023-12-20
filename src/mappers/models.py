from datetime import datetime
from ..database import Base
from sqlalchemy import TEXT, Column, DateTime, ForeignKey, Integer, String, Table

user_country_mapper = Table(
    "user_country_mapper",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("country_id", ForeignKey("country.id"), primary_key=True),
)
