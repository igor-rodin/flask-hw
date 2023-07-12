from fastapi import APIRouter, Query, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from models import Task, TaskIn, TaskUpdate
from bson.objectid import ObjectId
from pymongo import ReturnDocument

router = APIRouter()


def oid_to_str(item: dict):
    item["_id"] = str(item["_id"])
    return item


@router.get("/tasks", response_model=list[Task], response_model_exclude_none=True)
async def get_tasks(
    request: Request,
    skip: int = Query(default=0, title="Skip count", ge=0),
    count: int = Query(default=0, title="Get count", ge=0),
):
    tasks = request.app.db["tasks"].find(skip=skip, limit=count)
    tasks_ = list(tasks)
    tasks_ = list(map(oid_to_str, tasks_))
    return tasks_


@router.post("/tasks", response_model=Task)
async def create_task(task: TaskIn, request: Request):
    task = task.model_dump(exclude_none=True)
    inserted_id = request.app.db["tasks"].insert_one(task).inserted_id
    task["_id"] = str(inserted_id)
    return task


@router.get("/tasks/{task_id}", response_model=Task, response_model_exclude_none=True)
async def get_task_by_id(task_id: str, request: Request):
    task = request.app.db["tasks"].find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task["_id"] = str(task["_id"])
    return task


@router.put(
    "/tasks/{task_id}", response_model=TaskUpdate, response_model_exclude_none=True
)
async def update_task(task_id: str, task: TaskUpdate, request: Request):
    task = {key: val for key, val in task.model_dump().items() if val is not None}
    if task:
        upd_task = request.app.db["tasks"].find_one_and_update(
            {"_id": ObjectId(task_id)},
            {"$set": task},
            return_document=ReturnDocument.AFTER,
        )

        if upd_task:
            upd_task["_id"] = str(upd_task["_id"])
            return upd_task
    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: str, request: Request):
    res = request.app.db["tasks"].delete_one({"_id": ObjectId(task_id)})
    if res.deleted_count > 0:
        return {"message": "Task was successfully deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
