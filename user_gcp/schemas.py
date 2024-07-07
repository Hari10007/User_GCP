from pydantic import BaseModel
from typing import Optional
from datetime import date


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    project_id: Optional[int] = None
    company_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    mobile_number: Optional[str] = None
    date_of_birth: Optional[date] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
