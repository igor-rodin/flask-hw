from tasks.model import Task, TaskModel

tasks = [
    {"id": 1, "title": "Title", "description": "First task", "status": "todo"},
    {"id": 2, "title": "Title 2", "status": "in progress"},
    {"id": 3, "title": "Title 2", "description": "Another task", "status": "todo"},
]


def get_next_id() -> int:
    return max(tasks, key=lambda x: x.get("id")).get("id") + 1


def task_exist(id: int) -> bool:
    return True if [t for t in tasks if t.get("id") == id] else False


def get_task_by_id(id: int) -> Task | None:
    task = [t for t in tasks if t.get("id") == id]
    return Task(**task[0]) if task else None


def add_task(task: Task) -> None:
    tasks.append(task.model_dump())


def update_task(id: int, task: TaskModel) -> Task:
    updated_task = [t for t in tasks if t.get("id") == id]
    updated_task[0].update({"title": task.title})
    updated_task[0].update({"description": task.description})
    updated_task[0].update({"status": task.status})

    return Task(id=id, **task.model_dump())


def del_task(id: int):
    deleted_task = [t for t in tasks if t.get("id") == id]
    task = Task(**deleted_task[0])
    tasks.remove(deleted_task[0])
    return task
