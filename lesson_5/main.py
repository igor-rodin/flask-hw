from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, EmailStr
from typing import Optional
from tasks.model import Task, TaskModel
import tasks.db_fake as dbtask

app = FastAPI(title="Lesson 5 App")


"""

email: EmailStr = Field(..., description="Email address of the user")
    password: str = Field(..., min_length=8, regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).*$", description="Password of the user")
"""


@app.get(
    "/tasks",
    response_model=list[Task],
    tags=["Задачи"],
    summary="Получить список задач",
)
async def get_tasks():
    return dbtask.tasks


@app.get(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Задачи"],
    summary="Получить информацию о задаче по её id",
)
async def get_task(task_id: int):
    task = dbtask.get_task_by_id(task_id)
    if task:
        return task
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.post(
    "/tasks",
    response_model=Task,
    tags=["Задачи"],
    summary="Создать задачу",
)
async def create_task(task: TaskModel):
    next_id = dbtask.get_next_id()
    new_task = Task(id=next_id, **task.model_dump())
    dbtask.add_task(new_task)
    return new_task


@app.put(
    "/tasks/{task_id}",
    tags=["Задачи"],
    response_model=Task,
    summary="Обновить информацию о задаче по её id",
)
async def update_task(task_id: int, task: TaskModel):
    if not dbtask.task_exist(task_id):
        raise HTTPException(status_code=404, detail="Задача не найдена")
    updated = dbtask.update_task(task_id, task)

    return updated


@app.delete(
    "/tasks/{task_id}",
    response_model=Task,
    tags=["Задачи"],
    summary="Удалить задачу по её id",
)
async def delete_task(task_id: int):
    if dbtask.task_exist(task_id):
        return dbtask.del_task(task_id)
    raise HTTPException(status_code=404, detail="Задача не найдена")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
