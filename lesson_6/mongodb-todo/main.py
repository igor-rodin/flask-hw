from pymongo import MongoClient
from settings import settings
from fastapi import FastAPI, Query, HTTPException
import tasks
import uvicorn


app = FastAPI(title="Tasks MongoDB")

app.include_router(tasks.router, tags=["Tasks"])


@app.on_event("startup")
async def startup():
    app.mongo_client = MongoClient(settings.DATABASE_URL)
    app.db = app.mongo_client[settings.DATABASE_NAME]


@app.on_event("shutdown")
async def shutdown():
    app.mongo_client.close()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
