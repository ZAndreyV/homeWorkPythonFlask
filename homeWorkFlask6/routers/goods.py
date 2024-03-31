import random
from fastapi import APIRouter
from lorem.text import TextLorem

from homeWorkFlask6.db import goods, database
from homeWorkFlask6.models.goods import Goods, GoodsIn

router = APIRouter()


@router.get("/fake_goods/{count}")
async def create_goods(count: int):
    for i in range(count):
        query = goods.insert().values(
            name_of_goods=f"goods{i}",
            description=f"{TextLorem(srange=(5, 10)).sentence()}",
            price=random.randint(100, 9000) * .1,
        )
        await database.execute(query)
    return {"message": f"{count} fake goods create"}


@router.post("/goods/", response_model=GoodsIn)
async def create_goods(item: GoodsIn):
    query = goods.insert().values(
        name_of_goods=item.name_of_goods,
        description=item.description,
        price=item.price,
    )
    last_record_id = await database.execute(query)
    return {**item.dict(), "id": last_record_id}


@router.get("/goods/", response_model=list[Goods])
async def read_goods():
    query = goods.select()
    return await database.fetch_all(query)


@router.get("/goods/{item_id}", response_model=Goods)
async def read_user(item_id: int):
    query = goods.select().where(goods.c.id == item_id)
    return await database.fetch_one(query)


@router.put("/goods/{item_id}", response_model=Goods)
async def update_goods(item_id: int, new_item: GoodsIn):
    query = goods.update().where(goods.c.id == item_id).values(**new_item.dict())
    await database.execute(query)
    return {**new_item.dict(), "id": item_id}


@router.delete("/goods/{item_id}")
async def delete_user(item_id: int):
    query = goods.delete().where(goods.c.id == item_id)
    await database.execute(query)
    return {"message": "Item deleted"}
