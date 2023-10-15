from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    age: int
    user_info: str | None = None


class UserAuth(BaseModel):
    username: str
    password: str


class IsAdult(User):
    is_adult: bool = False


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
