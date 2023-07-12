from typing import Optional
from pydantic import BaseModel, Field
from settings import settings
from bson.objectid import ObjectId


class TaskIn(BaseModel):
    title: str = Field(
        ..., min_length=settings.TITLE_MIN_LENGTH, max_length=settings.TITLE_MAX_LENGTH
    )
    description: Optional[str] = Field(
        default=None, max_length=settings.DESCRIPTION_MAX_LENGTH
    )
    done: bool = Field(default=False, description="Статус задачи")


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(
        min_length=settings.TITLE_MIN_LENGTH, max_length=settings.TITLE_MAX_LENGTH
    )
    description: Optional[str] = Field(
        default=None, max_length=settings.DESCRIPTION_MAX_LENGTH
    )
    done: Optional[bool] = Field(default=False, description="Статус задачи")


class Task(TaskIn):
    id: str = Field(..., alias="_id")

    class Config:
        allow_population_by_name = True
