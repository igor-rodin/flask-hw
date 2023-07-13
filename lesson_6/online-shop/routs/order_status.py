from fastapi import APIRouter, Query, HTTPException
from models.order_status import OrderStatus, OrderStatusIn
from database import order_status, db

router = APIRouter()


@router.get("/order-status", response_model=list[OrderStatus])
async def get_status():
    query = order_status.select()
    return await db.fetch_all(query=query)


@router.post("/order-status}", response_model=OrderStatus)
async def create_status(status: OrderStatusIn):
    query = order_status.insert().values(**status.model_dump(exclude_none=True))
    id = await db.execute(query=query)
    return OrderStatus(**status.model_dump(), id=id)


@router.get("/order-status/{status_id}", response_model=OrderStatus)
async def get_status_by_id(status_id: int):
    query = order_status.select().where(order_status.c.id == status_id)
    data = await db.fetch_one(query=query)
    if not data:
        raise HTTPException(status_code=404, detail="Order status not found")
    return data


@router.put("/order-status/{status_id}", response_model=OrderStatus)
async def update_status(status_id: int, product: OrderStatusIn):
    query = (
        order_status.update()
        .where(order_status.c.id == status_id)
        .values(**product.model_dump(exclude_none=True))
    )
    res = await db.execute(query=query)
    if res > 0:
        query = order_status.select().where(order_status.c.id == status_id)
        data = await db.fetch_one(query=query)
        return data
    raise HTTPException(status_code=404, detail="Order status not found")


@router.delete("/order-status/{status_id}", response_model=dict)
async def delete_status(status_id: int):
    query = order_status.delete().where(order_status.c.id == status_id)
    res = await db.execute(query=query)
    if res > 0:
        return {"message": "Product was successfully deleted"}
    raise HTTPException(status_code=404, detail="Order status not found")
