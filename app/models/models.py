from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    age: int
    user_info: str | None = None


class IsAdult(User):
    is_adult: bool = False
