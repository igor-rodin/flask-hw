import uuid
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from tasks.model import Task, TaskModel
from users.model import UserOut, User, UserIn
import tasks.db_fake as dbtask
import users.db_fake as dbusers

app = FastAPI(title="Урок 5. Знакомство с FastAPI")
app.mount("/static", StaticFiles(directory="lesson_5/public"), name="static")
templates = Jinja2Templates(directory="lesson_5/public/templates")

"""
    Задание №6
    API для работы с пользователями
"""


@app.get("/", response_class=RedirectResponse, tags=["Пользователи"], summary="Главная")
async def index():
    return "/users"


@app.get(
    "/users",
    response_class=HTMLResponse,
    tags=["Пользователи"],
    summary="Получение списка пользователей",
)
async def get_users(request: Request):
    users = dbusers.get_users()

    return templates.TemplateResponse(
        "users.html", {"request": request, "users": users, "caption": "Пользователи"}
    )


@app.post(
    "/users",
    response_model=UserOut,
    tags=["Пользователи"],
    summary="Создать пользователя",
)
async def create_user(user: UserIn):
    if dbusers.user_exist(user.email):
        raise HTTPException(
            status_code=409, detail="Данный email уже зарегистриован. Выберите другой"
        )
    new_user = User(
        **user.model_dump(exclude="password"), id=uuid.uuid4(), password_hash=""
    )
    new_user.set_password(user.password)
    dbusers.add_user(new_user)

    return UserOut(**new_user.model_dump(exclude=["id", "password_hash"]))


@app.get(
    "/users/{user_email}",
    response_model=UserOut,
    tags=["Пользователи"],
    summary="Получить информацию о пользователе по его email",
)
async def get_user(user_email: str):
    user = dbusers.get_user_by_email(user_email)
    if user:
        return UserOut(**user.model_dump(exclude=["id", "password_hash"]))
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app.put(
    "/users/{user_email}",
    tags=["Пользователи"],
    response_model=UserOut,
    summary="Обновить информацию о пользователе по его email",
)
async def update_user(user_email: str, user: UserIn):
    if not dbusers.user_exist(user_email):
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    if dbusers.user_exist(user.email) and user_email != user.email:
        raise HTTPException(
            status_code=409, detail="Данный email уже зарегистриован. Выберите другой"
        )
    new_data = User(**user.model_dump(), password_hash="")
    new_data.set_password(user.password)
    updated = dbusers.update_user(user_email, new_data)

    return updated


@app.delete(
    "/users/{user_email}",
    response_model=UserOut,
    tags=["Пользователи"],
    summary="Удалить пользователе по его email",
)
async def delete_user(user_email: str):
    if dbusers.user_exist(user_email):
        return dbusers.del_user(user_email)
    raise HTTPException(status_code=404, detail="Пользователь не найден")


"""
    Задание №7
    API для управления списком задач
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
