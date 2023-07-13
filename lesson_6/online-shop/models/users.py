from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from settings import settings


class UserIn(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=settings.NAME_MAX_LENGTH)
    last_name: Optional[str] = Field(
        default=None, min_length=2, max_length=settings.NAME_MAX_LENGTH
    )
    email: EmailStr = Field(..., max_length=settings.EMAIL_MAX_LENGTH)
    password: str = Field(..., min_length=settings.PASSWORD_MIN_LENGTH)


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(
        default=None, min_length=2, max_length=settings.NAME_MAX_LENGTH
    )
    last_name: Optional[str] = Field(
        default=None, min_length=2, max_length=settings.NAME_MAX_LENGTH
    )
    email: Optional[EmailStr] = Field(
        default=None, max_length=settings.EMAIL_MAX_LENGTH
    )


class User(UserUpdate):
    id: int
