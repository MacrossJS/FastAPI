import uvicorn
from fastapi import FastAPI, Depends

app = FastAPI()

# фейковая БД для хранения пользовательских данных
fake_database = {
    1: {"id": 1, "name": "John Doe"},
    2: {"id": 2, "name": "Jane Smith"},
}


# Функция зависимости для получения экземпляра базы
def get_database():
    return fake_database


# Функция маршрутизации с внедрением зависимостей (dependency injection)
@app.get("/users/{user_id}")
def get_user(user_id: int, database: dict = Depends(get_database)):
    if user_id in database:
        return database[user_id]
    else:
        return {"message": "User not found"}


# Другая функция маршрутизации с тем же внедрением зависимостей
@app.get("/users/")
def get_all_users(database: dict = Depends(get_database)):
    return list(database.values())


if __name__ == "__main__":
    uvicorn.run("main_1:app", host='127.0.0.1', port=8066, reload=True, workers=3)
