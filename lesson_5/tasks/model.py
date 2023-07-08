import enum
from pydantic import BaseModel, EmailStr
from typing import Optional


class Status(enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in progress"
    DONE = "done"


class TaskModel(BaseModel):
    title: str
    description: Optional[str] = None
    status: Status = Status.TODO


class Task(TaskModel):
    id: int
