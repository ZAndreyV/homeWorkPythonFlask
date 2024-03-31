import random
from fastapi import APIRouter
from sqlalchemy import select

from homeWorkFlask6.db import users, database
from homeWorkFlask6.models.user import UserIn, User, UserFront

router = APIRouter()


@router.get("/fake_users/{count}")
async def create_note(count: int):
    for i in range(count):
        query = users.insert().values(
            name=f"user{i}",
            surname=f"surname{i}",
            email=f"mail{i}@mail.ru",
            password=f'{"".join([str(random.randint(1, 9)) for i in range(7)])}',
        )
        await database.execute(query)
    return {"message": f"{count} fake users create"}


@router.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=user.password,
    )
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@router.get("/users/", response_model=list[UserFront])
async def read_users():
    query = select(
        users.c.id,
        users.c.name,
        users.c.surname,
        users.c.email,
    )
    return await database.fetch_all(query)


@router.get("/users/{user_id}", response_model=UserFront)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {"message": "User deleted"}
