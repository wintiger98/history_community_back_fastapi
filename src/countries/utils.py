from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .schema import CountryInput, CountryOutput
from .models import Country
from ..database import get_db


def make_country():
    pass


def get_countries():
    pass


def update_country():
    pass


def erase_country():
    pass
