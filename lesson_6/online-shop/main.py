from fastapi import FastAPI
from database import db
import routs.users as users
import routs.products as products
import routs.order_status as status
import routs.orders as orders
import uvicorn


app = FastAPI(title="Lesson 6. Online shop")

app.include_router(users.router, tags=["Users"])
app.include_router(products.router, tags=["Products"])
app.include_router(status.router, tags=["Order Status"])
app.include_router(orders.router, tags=["Orders"])


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
