from fastapi import APIRouter, Query, HTTPException
from models.users import User, UserIn, UserUpdate
from models.products import Product
from models.order_status import OrderStatus
from models.orders import Order, OrderOut
from database import users, orders, products, order_status, db
from bcrypt import gensalt, hashpw

router = APIRouter()


def parse_user_order_row_(order) -> OrderOut:
    return OrderOut(
        id=order.id,
        products_amount=order.products_amount,
        order_date=order.order_date,
        product=Product(
            id=order.product_id,
            product_name=order.product_name,
            description=order.description,
            price=order.price,
        ),
        status=OrderStatus(id=order.order_status, status_name=order.status_name),
    )


@router.get("/users", response_model=list[User], response_model_exclude_none=True)
async def get_users(
    skip: int = Query(default=None, title="Skip count", ge=0),
    count: int = Query(default=None, title="Get count", gt=0),
):
    query = users.select().offset(skip).limit(count)
    return await db.fetch_all(query=query)


@router.post("/users", response_model=User)
async def create_user(user: UserIn):
    salt = gensalt()
    password_hash = hashpw(user.password.encode("utf-8"), salt=salt)
    user.password = password_hash.decode("utf-8")
    query = users.insert().values(**user.model_dump())
    user_id = await db.execute(query=query)
    return User(**user.model_dump(), id=user_id)


@router.get("/users/{user_id}", response_model=User, response_model_exclude_none=True)
async def get_user_by_id(user_id: int):
    query = users.select().where(users.c.id == user_id)
    data = await db.fetch_one(query=query)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    return data


@router.get(
    "/users/{user_id}/orders",
    response_model=list[OrderOut],
    summary="List user's orders",
)
async def get_users_order_by_id(user_id: int):
    join_query = (
        orders.join(users)
        .join(products)
        .join(order_status)
        .select()
        .where(orders.c.user_id == user_id)
    )
    data = await db.fetch_all(query=join_query)
    if not data:
        raise HTTPException(status_code=404, detail="Orders not found")
    return list(map(parse_user_order_row_, data))


@router.put("/users/{user_id}", response_model=User, response_model_exclude_none=True)
async def update_user(user_id: int, user: UserUpdate):
    query = (
        users.update()
        .where(users.c.id == user_id)
        .values(**user.model_dump(exclude_none=True))
    )
    res = await db.execute(query=query)
    if res > 0:
        query = users.select().where(users.c.id == user_id)
        data = await db.fetch_one(query=query)
        return data
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    res = await db.execute(query=query)
    if res > 0:
        return {"message": "User was successfully deleted"}
    raise HTTPException(status_code=404, detail="User not found")
