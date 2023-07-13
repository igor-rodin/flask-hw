from fastapi import APIRouter, Query, HTTPException
from models.products import Product
from models.users import User
from models.order_status import OrderStatus
from models.orders import Order, OrderIn, OrderUpdate
from database import products, orders, order_status, users, db

router = APIRouter()


def parse_order_row_(order) -> Order:
    res = Order(
        id=order.id,
        products_amount=order.products_amount,
        order_date=order.order_date,
        product=Product(
            id=order.product_id,
            product_name=order.product_name,
            description=order.description,
            price=order.price,
        ),
        user=User(
            id=order.user_id,
            first_name=order.first_name,
            last_name=order.last_name,
            email=order.email,
        ),
        status=OrderStatus(id=order.order_status, status_name=order.status_name),
    )
    return res


@router.get("/orders", response_model=list[Order], response_model_exclude_none=True)
async def get_orders(
    skip: int = Query(default=None, title="Skip count", ge=0),
    count: int = Query(default=None, title="Get count", gt=0),
):
    join_query = (
        orders.join(users)
        .join(products)
        .join(order_status)
        .select()
        .offset(skip)
        .limit(count)
    )
    join_res = await db.fetch_all(query=join_query)
    return list(map(parse_order_row_, join_res))


@router.post("/orders", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(**order.model_dump(exclude_none=True))
    new_id = await db.execute(query=query)
    join_query = (
        orders.join(users)
        .join(products)
        .join(order_status)
        .select()
        .where(orders.c.id == new_id)
    )
    join_res = await db.fetch_all(query=join_query)

    return parse_order_row_(join_res[0])


@router.get("/orders/{order_id}", response_model=Order)
async def get_order_by_id(order_id: int):
    join_query = (
        orders.join(users)
        .join(products)
        .join(order_status)
        .select()
        .where(orders.c.id == order_id)
    )
    data = await db.fetch_all(query=join_query)
    if not data:
        raise HTTPException(status_code=404, detail="Order not found")
    return parse_order_row_(data[0])


@router.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order: OrderUpdate):
    query = (
        orders.update()
        .where(orders.c.id == order_id)
        .values(**order.model_dump(exclude_none=True))
    )
    res = await db.execute(query=query)
    if res > 0:
        join_query = (
            orders.join(users)
            .join(products)
            .join(order_status)
            .select()
            .where(orders.c.id == order_id)
        )
        data = await db.fetch_all(query=join_query)
        return parse_order_row_(data[0])
    raise HTTPException(status_code=404, detail="Order not found")


@router.delete("/orders/{order_id}", response_model=dict)
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    res = await db.execute(query=query)
    if res > 0:
        return {"message": "Order was successfully deleted"}
    raise HTTPException(status_code=404, detail="Order not found")
