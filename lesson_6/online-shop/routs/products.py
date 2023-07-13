from fastapi import APIRouter, Query, HTTPException
from models.products import Product, ProductIn, ProductUpdate
from database import products, db

router = APIRouter()


@router.get("/products", response_model=list[Product], response_model_exclude_none=True)
async def get_products(
    skip: int = Query(default=None, title="Skip count", ge=0),
    count: int = Query(default=None, title="Get count", gt=0),
):
    query = products.select().offset(skip).limit(count)
    return await db.fetch_all(query=query)


@router.post("/products", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(**product.model_dump(exclude_none=True))
    product_id = await db.execute(query=query)
    return Product(**product.model_dump(), id=product_id)


@router.get(
    "/products/{product_id}", response_model=Product, response_model_exclude_none=True
)
async def get_product_by_id(product_id: int):
    query = products.select().where(products.c.id == product_id)
    data = await db.fetch_one(query=query)
    if not data:
        raise HTTPException(status_code=404, detail="Product not found")
    return data


@router.put(
    "/products/{product_id}", response_model=Product, response_model_exclude_none=True
)
async def update_product(product_id: int, product: ProductUpdate):
    query = (
        products.update()
        .where(products.c.id == product_id)
        .values(**product.model_dump(exclude_none=True))
    )
    res = await db.execute(query=query)
    if res > 0:
        query = products.select().where(products.c.id == product_id)
        data = await db.fetch_one(query=query)
        return data
    raise HTTPException(status_code=404, detail="Product not found")


@router.delete("/products/{product_id}", response_model=dict)
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    res = await db.execute(query=query)
    if res > 0:
        return {"message": "Product was successfully deleted"}
    raise HTTPException(status_code=404, detail="Product not found")
