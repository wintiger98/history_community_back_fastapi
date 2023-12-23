from typing import Optional
from pydantic import BaseModel


class CountryBase(BaseModel):
    name: str


class CountryInput(CountryBase):
    pass


class CountryOutput(CountryBase):
    id: int


# class CountryOneOutput(CountryOutput):
#     cheers: int
