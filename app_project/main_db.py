import uvicorn
from fastapi import FastAPI, HTTPException
from databases import Database
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# URL для PostgreSQL (измените его под свою БД)
DATABASE_URL = "postgresql://user:password@localhost/dbname"
DATABASE_URL = "postgresql://postgres:226ffoGFV226!@localhost/postgres"
database = Database(DATABASE_URL)


# Модель User для валидации входных данных
class UserCreate(BaseModel):
    username: str
    email: str


# Модель User для валидации исходящих данных
class UserReturn(BaseModel):
    username: str
    email: str
    id: Optional[int] = None


# тут устанавливаем условия подключения к базе данных и отключения
@app.on_event("startup")
async def startup_database():
    await database.connect()


@app.on_event("shutdown")
async def shutdown_database():
    await database.disconnect()


# создание роута для создания юзеров
@app.post("/users/", response_model=UserReturn)
async def create_user(user: UserCreate):
    query = "INSERT INTO fastapi_users (username, email) VALUES (:username, :email) RETURNING id"
    values = {"username": user.username, "email": user.email}
    try:
        user_id = await database.execute(query=query, values=values)
        return {**user.model_dump(), "id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create user")


# маршрут для получения информации о юзере по ID
@app.get("/user/{user_id}", response_model=UserReturn)
async def get_user(user_id: int):
    query = "SELECT * FROM fastapi_users WHERE id = :user_id"
    values = {"user_id": user_id}
    try:
        result = await database.fetch_one(query=query, values=values)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user from database: {e}")
    if result:
        return UserReturn(username=result["username"], email=result["email"])
    else:
        raise HTTPException(status_code=404, detail="User not found")


if __name__ == "__main__":
    uvicorn.run("main_db:app", host='127.0.0.1', port=8000, reload=True)
