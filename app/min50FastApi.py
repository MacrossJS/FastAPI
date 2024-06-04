import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from database50 import create_tables, delete_tables
from router import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова")
    yield
    await delete_tables()
    print("База очищена")


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)

tasks = []

if __name__ == "__main__":
    uvicorn.run("min50FastApi:app", host='127.0.0.1', port=8066, reload=True, workers=3)
    # uvicorn.run("min50FastApi:app", host='127.0.0.1', port=8000, reload=True)
