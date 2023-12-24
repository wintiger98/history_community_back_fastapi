from typing import List
from fastapi import APIRouter, HTTPException, Depends, Form, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from .utils import erase_country, get_countries, make_country, update_country
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
    filters = {id: country_id}
    country = get_countries(filters=filters, db=db)
    if not country:
        raise HTTPException(status_code=404, detail="Not found country")
    if len(country) > 1:
        raise HTTPException(status_code=400, detail="Invalid country id")
    return country[0]


@router.put("/{country_id}")
async def put_country(
    country_id: int, data: CountryInput, db: Session = Depends(get_db)
):
    filters = {id: country_id}
    country = get_countries(filters=filters, db=db)
    if not country:
        raise HTTPException(status_code=404, detail="Not found country")
    if len(country) > 1:
        raise HTTPException(status_code=400, detail="Invalid country id")
    country = country[0]
    result = update_country(data=data, country=country, db=db)
    if result["result"]:
        return {"detail": "Country updated"}
    else:
        raise HTTPException(status_code=400, detail=result["detail"])


@router.delete("/{country_id}")
async def delete_country(country_id: int, db: Session = Depends(get_db)):
    filters = {id: country_id}
    country = get_countries(filters=filters, db=db)
    if not country:
        raise HTTPException(status_code=404, detail="Not found country")
    if len(country) > 1:
        raise HTTPException(status_code=400, detail="Invalid country id")
    country = country[0]

    if erase_country(country=country, db=db):
        return {"detail": "Country deleted"}
    else:
        raise HTTPException(status_code=400, detail="Country delete failed")


@router.post("/{country_id}/cheer")
async def cheer_country(db: Session = Depends(get_db)):
    pass
