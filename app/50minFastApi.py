from fastapi import FastAPI, Depends
import uvicorn
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()


class STaskAdd(BaseModel):
    name: str
    description: str | None


class STask(STaskAdd):
    id: int


tasks = []


@app.post("/tasks")
async def add_task(task: Annotated[STaskAdd, Depends()]):
    tasks.append(task)
    return {'ok': True}


@app.get("/tasks")
def get_tasks():
    task = STask(name="Разведи на нюдсы")
    return {"data": "Hello, World"}


if __name__ == "__main__":
    uvicorn.run("50minFastApi:app", host='127.0.0.1', port=8000, reload=True)
