from typing import List
from fastapi import APIRouter, HTTPException, Depends, Form, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth.models import User
from ..auth.utils import get_current_user
from .utils import (
    cheer,
    erase_country,
    get_countries,
    get_country_by_id,
    make_country,
    update_country,
)
from .schema import CountryOutput, CountryInput
from .models import Country, Cheer

router = APIRouter(
    prefix="/countries",
    tags=["countries"],
)


@router.post("", response_model=CountryOutput)
async def post_country(data: CountryInput, db: Session = Depends(get_db)):
    country = make_country(data=data, db=db)
    return country


@router.get("", response_model=List[CountryOutput])
async def get_all_countries(db: Session = Depends(get_db)):
    countries = get_countries(filters={}, db=db)
    return countries


@router.get("/{country_id}", response_model=CountryOutput)
async def get_country(country_id: int, db: Session = Depends(get_db)):
    return get_country_by_id(country_id=country_id, db=db)


@router.put("/{country_id}")
async def put_country(
    country_id: int, data: CountryInput, db: Session = Depends(get_db)
):
    country = get_country_by_id(country_id=country_id, db=db)
    result = update_country(data=data, country=country, db=db)
    if result["result"]:
        return {"detail": "Country updated"}
    else:
        raise HTTPException(status_code=400, detail=result["detail"])


@router.delete("/{country_id}")
async def delete_country(country_id: int, db: Session = Depends(get_db)):
    country = get_country_by_id(country_id=country_id, db=db)

    if erase_country(country=country, db=db):
        return {"detail": "Country deleted"}
    else:
        raise HTTPException(status_code=400, detail="Country delete failed")


@router.post("/{country_id}/cheer")
async def cheer_country(
    country_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # 국가 판별
    country = get_country_by_id(country_id=country_id, db=db)
    # 응원
    result = cheer(country=country, user=user, db=db)

    if result["result"]:
        return {"detail": result["detail"]}
    else:
        return {"detail": result["detail"]}
