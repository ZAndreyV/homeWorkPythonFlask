import random
from datetime import datetime
from fastapi import APIRouter
from homeWorkFlask6.db import orders, database, users, goods
from homeWorkFlask6.models.orders import OrderIn, Order

router = APIRouter()


@router.get("/create_test_orders/{count}")
async def create_test_orders(count: int):
    # 1 Формируем список
    query = users.select()
    list_users = await database.fetch_all(query)
    list_users_id = set()
    for user_ in list_users:
        list_users_id.add(user_[0])

    # 2 Формируем список ID номеров товаров
    query = goods.select()
    list_products = await database.fetch_all(query)
    list_products_id = []   # список id номера товаров
    for product_ in list_products:
        list_products_id.append(product_[0])

    # 3 Формируем закааы по ID номерам пользователей и товаров
    status_list = ["в сборке", "доставка", "ждет оплаты", "получен", "отменен", "решение спора", "в корзине"]
    for count_ in range(count):
        if not list_users_id:
            break
        id_user_ = random.choice(list(list_users_id))
        list_users_id.remove(id_user_)
        for count2_ in range(random.randint(2,10)):
            id_product_ = random.choice(list_products_id)
            status_=random.choice(status_list)
            query = orders.insert().values(user_id=id_user_,
                                           goods_id=id_product_,
                                           date=datetime.now(),
                                           status=status_)
            await database.execute(query)
            print(id_user_, id_product_, status_)
    return {"message": "test orders create"}


@router.post("/order/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(
        user_id=order.user_id,
        goods_id=order.goods_id,
        date=order.date,
        status=order.status
    )
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}


@router.get("/orders/", response_model=list[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@router.get("/order/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@router.put("/order/{order_id}", response_model=Order)
async def update_goods(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}


@router.delete("/order/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {"message": "Order deleted"}

