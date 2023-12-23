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
    country = make_country()
    return country


@router.get("", response_model=List[CountryOutput])
async def get_all_countries(db: Session = Depends(get_db)):
    countries = get_countries()
    return countries


@router.get("/{country_id}", response_class=CountryOutput)
async def get_country(country_id: int, db: Session = Depends(get_db)):
    country = get_countries()
    if not country:
        raise HTTPException(status_code=404, detail="Not found country")
    return country


@router.put("/{country_id}")
async def put_country(db: Session = Depends(get_db)):
    result = update_country()
    if result["result"]:
        return {"detail": "Country updated"}
    else:
        raise HTTPException(status_code=400, detail=result["detail"])


@router.delete("/{country_id}")
async def delete_country(db: Session = Depends(get_db)):
    if erase_country():
        return {"detail": "Country deleted"}
    else:
        raise HTTPException(status_code=400, detail="Country delete failed")


@router.post("/{country_id}/cheer")
async def cheer_country(db: Session = Depends(get_db)):
    pass
