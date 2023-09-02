from typing import Annotated
from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Cookie
from fastapi.responses import FileResponse
import uvicorn

from models.models import User, IsAdult, Item

app = FastAPI(title='My first App')

fake_db: dict = {1: {"id": 1, "name": 'Test', "age": 27, "user_info": "QA"},
                 2: {"id": 2, "name": 'Macross', "age": 34, "user_info": "Backend"},
                 3: {"id": 3, "name": 'Varvara', "age": 42, "user_info": "Frontend"}
                 }
items: list[Item] = [
    Item(name="Лада", price=88, description="Необычный черничный пирог в форме автомобиля"),
    Item(name="Portal Gun", price=42.0),
    Item(name="Plumbus", price=32.0),
]


@app.get("/")
def root():
    return FileResponse("index.html")


@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(default=None)):
    return {"ads_id": ads_id}


@app.post("/items/")
async def create_item(item: Item):
    return item


# новый роут
@app.get("/custom")
def read_custom_message():
    return {"message": "This is a custom message!"}


@app.get('/calculate/{item_id}')
async def calc(item_id: str):
    return {'result': eval(item_id)}


@app.get("/users/")
def read_users(limit: int = 10):
    return dict(sorted(fake_db.items())[:limit])


@app.post('/user')
async def is_adult(user: IsAdult):
    if user.age >= 18:
        user.is_adult = True
    print(user)
    return user


@app.post('/add_user')
async def add_user(name: str, age: int, user_info: str):
    next_id = sorted(fake_db.keys())[-1] + 1
    fake_db[next_id] = {
        "id": next_id,
        "name": name,
        "age": age,
        "user_info": user_info
    }
    return {"message": f"юзер {name} успешно добавлен в базу данных"}


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


@app.get('/users/{user_id}')  # тут объявили параметр пути
async def search_user_by_id(user_id: int):  # тут указали его тип данных
    return fake_db.get(user_id, {"error": f"Пользователь с id = {user_id} в базе не найден!"})


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8066, reload=True, workers=3)
