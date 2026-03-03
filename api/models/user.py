from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    full_name: Optional[str] = None
    email: EmailStr
    password: str
    dob: Optional[str] = None
    birth_place: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str
