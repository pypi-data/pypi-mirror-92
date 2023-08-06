from pydantic import BaseModel, constr, EmailStr
from typing import Optional, List
from .base import patients, doctors

class UserIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class UserDB(BaseModel):
    id: int
    public_key: constr(max_length=20)
    email: EmailStr
    hashed_password: str

    class Config:
        orm_mode = True


class UserOut(BaseModel):
   public_key: constr(max_length=20)
   email: EmailStr



   class Config:
       orm_mode = True