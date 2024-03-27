"""
Задание

Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание.
Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).

API должен содержать следующие конечные точки:
— GET /tasks — возвращает список всех задач.
— GET /tasks/{id} — возвращает задачу с указанным идентификатором.
— POST /tasks — добавляет новую задачу.
— PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
— DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.

Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
Для этого использовать библиотеку Pydantic.
"""

from typing import Optional
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()
tasks = []


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str


class TaskIn(BaseModel):
    title: str
    description: Optional[str]
    status: str


@app.get("/tasks/", response_model=list[Task])
async def all_tasks():
    return tasks


@app.get('/tasks/{id}', response_model=Task)
async def find_task(find_id: int):
    for i in range(len(tasks)):
        if tasks[i].id == find_id:
            return tasks[i]
    raise HTTPException(status_code=404, detail='Task not found')


@app.post("/tasks/", response_model=list[Task])
async def create_task(new_task: TaskIn):
    tasks.append(
        Task(
            id=len(tasks) + 1,
            title=new_task.title,
            description=new_task.description,
            status=new_task.status,
        )
    )
    return tasks


@app.put("/tasks/", response_model=Task)
async def edit_task(task_id: int, new_task: TaskIn):
    for i in range(len(tasks)):
        if tasks[i].id == task_id:
            current_task = tasks[i]
            current_task.title = new_task.title
            current_task.description = new_task.description
            current_task.status = new_task.status
            return current_task
    raise HTTPException(status_code=404, detail='Task not found')


@app.delete("/tasks/", response_model=dict)
async def delete_task(task_id: int):
    for i in range(len(tasks)):
        if tasks[i].id == task_id:
            tasks.remove(tasks[i])
            return {'message': 'Task was deleted'}
    raise HTTPException(status_code=404, detail='Task not found')


if __name__ == "__main__":
    uvicorn.run("task_1:app", host="127.0.0.1", port=8000, reload=True)