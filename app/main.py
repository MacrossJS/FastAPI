from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn

from models.models import User, IsAdult

title = 'My first App'
app = FastAPI(title=title)

fake_db = [User(id=1, name='Test', age=27, user_info="QA"),
           User(id=2, name='Macross', age=34, user_info="Backend"),
           User(id=3, name='Varvara', age=42, user_info="Frontend")]


@app.get("/")
def root():
    return FileResponse("index.html")


# новый роут
@app.get("/custom")
def read_custom_message():
    return {"message": "This is a custom message!"}


@app.get('/calculate/{item_id}')
async def calc(item_id: str):
    return {'result': eval(item_id)}


# @app.post("/")
# async def root(user: User):
#     """тут"""
#     print(f'Мы получили от юзера {user.username} такое сообщение: {user.message}')
#     return user


@app.get("/users")  # , response_model=User)
def user_root():
    return fake_db


@app.post('/user')
async def is_adult(user: IsAdult):
    if user.age >= 18:
        user.is_adult = True
    print(user)
    return user


@app.get('/{user_id}')  # тут объявили параметр пути
async def search_user_by_id(user_id: int):  # тут указали его тип данных
    for user in fake_db:
        if user.id == user_id:
            return user
    return {"error": f"Пользователь с id = {user_id} в базе не найден!"}


@app.post('/add_user')
async def add_user(name: str, age: int, user_info: str):
    fake_db.append(User(
        id=fake_db[-1].id + 1,
        name=name,
        age=age,
        user_info=user_info))
    return {"message": f"юзер {name} успешно добавлен в базу данных"}


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8066, reload=True, workers=3)
