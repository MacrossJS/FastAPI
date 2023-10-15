from typing import Annotated
from fastapi import FastAPI, Request, HTTPException, Depends, status, File, UploadFile, BackgroundTasks, Cookie
from fastapi.responses import FileResponse, Response
import uvicorn
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from models.models import User, IsAdult, Item, UserAuth

app = FastAPI(title='My first App')
security = HTTPBasic()

fake_db: dict = {1: {"id": 1, "name": 'Test', "age": 27, "user_info": "QA"},
                 2: {"id": 2, "name": 'Macross', "age": 34, "user_info": "Backend"},
                 3: {"id": 3, "name": 'Varvara', "age": 42, "user_info": "Frontend"}
                 }
# добавим симуляцию базы данных в виде массива объектов юзеров
USER_DATA = [UserAuth(**{"username": "user1", "password": "pass1"}),
             UserAuth(**{"username": "user2", "password": "pass2"})]

items: list[Item] = [
    Item(name="Лада", price=88, description="Необычный черничный пирог в форме автомобиля"),
    Item(name="Portal Gun", price=42.0),
    Item(name="Plumbus", price=32.0),
]


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Basic"})
    return user


# симуляционный пример
def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
    return None


@app.get("/login/")
def get_protected_resource(user: UserAuth = Depends(authenticate_user)):
    response = Response("You got my secret, welcome")
    response.headers["WWW-Authenticate"] = "Basic"
    response.status_code = status.HTTP_401_UNAUTHORIZED
    return {"message": "You have access to the protected resource!",
            "user_info": user, "response": response}


@app.get("/")
def root():
    return FileResponse("index.html")


@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(default=None)):
    return {"ads_id": ads_id}


# Заголовки
@app.get("/headers")
async def get_headers(request: Request):
    user_agent = request.headers.get("user-agent")
    accept_language = request.headers.get("accept-language")
    print(request.headers)
    if user_agent is None or accept_language is None:
        raise HTTPException(status_code=400, detail="Missing required headers")

    response_data = {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }

    return response_data


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
