from typing import Optional, Annotated

import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field


app = FastAPI()


class UserModel(BaseModel):
    username: str
    age: int = Field(gt=18)
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)
    phone: Optional[str] = "Unknown"


custom_messages = {
    "username": "Имя должно быть строкой",
    "age": "Возраст должен быть более 18",
    "email": "Ошибка в записи email",
    "password": "Длина пароля должна быть от 8 до 16 символов",
    "phone": "В качестве номера телефона ожидается строка",
}


@app.exception_handler(RequestValidationError)
def custom_request_validation_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = error["loc"][-1]
        msg = custom_messages.get(field)
        errors.append({"field": field, "msg": msg, "value": error["input"]})
    print(errors)
    return JSONResponse(status_code=400, content=errors)


@app.post("/users/")
async def post_user(user: Annotated[UserModel, Depends()]):
    return user

if __name__ == "__main__":
    uvicorn.run("main_errors:app", host='127.0.0.1', port=8066, reload=True, workers=3)
