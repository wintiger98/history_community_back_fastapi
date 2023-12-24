from fastapi import Depends, HTTPException, status
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from .schema import CountryInput, CountryOutput
from .models import Country
from ..database import get_db


def make_country(data: CountryInput, db: Session):
    new_country = Country(**data.model_dump())

    db.add(new_country)
    db.commit()
    db.refresh(new_country)

    return new_country


def get_countries(filters: dict, db: Session):
    and_list = []
    for key, value in filters.items():
        and_list.append(getattr(Country, key) == value)

    stmt = select(Country).where(and_(*and_list))
    result = db.execute(stmt)
    countries = result.scalars().all()
    return countries


def update_country(data: CountryInput, country: Country, db: Session):
    try:
        for key, value in data.model_dump().items():
            if value:
                setattr(country, key, value)
    except:
        return {"result": False, "detail": "country update failed"}
    try:
        db.commit()
    except:
        return {
            "result": False,
            "detail": "database commit failed while updating country",
        }
    return {"result": True}


def erase_country(country: Country, db: Session):
    try:
        db.delete(country)
        db.commit()

        return True
    except:
        return False
