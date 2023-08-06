import datetime
from pydantic import BaseModel, constr
from typing import Optional, TypeVar, List
from .base import patients


class DoctorIn(BaseModel):
    fullname: constr(max_length=100)
    birthdate: datetime.date
    gender: constr(max_length=2)

    class Config:
        orm_mode = True


class DoctorDB(BaseModel):
    id: int
    public_key: constr(max_length=20)
    fullname: constr(max_length=100)
    birthdate: datetime.date
    gender: constr(max_length=2)

    class Config:
        orm_mode = True


class DoctorOut(BaseModel):
    fullname: constr(max_length=100)
    birthdate: datetime.date
    gender: constr(max_length=2)
    public_key: constr(max_length=20)

    class Config:
        orm_mode = True