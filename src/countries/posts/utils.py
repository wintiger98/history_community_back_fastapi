from fastapi import Depends, HTTPException, status
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from ...auth.models import User
from ..models import Country

def check_country(country_id: int, db: Session):
    stmt = select(Country).where(Country.id == country_id)
    result = db.execute(stmt)
    country = result.scalar()
    return country