from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import JWTStrategy, CookieTransport, AuthenticationBackend
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import SessionLocal, Base, engine
from models import User as UserModel
from schemas import UserCreate, UserUpdate, UserDB
from typing import Optional

class UserManager(BaseUserManager[UserModel, int]):
    user_db_model = UserModel

    async def on_after_register(self, user: UserModel, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def get_by_username(self, username: str):
        async with SessionLocal() as session:
            query = await session.execute(select(UserModel).where(UserModel.username == username))
            return query.scalars().first()

async def get_user_db(session: AsyncSession = Depends(SessionLocal)):
    yield SQLAlchemyUserDatabase(session, UserModel)

cookie_transport = CookieTransport(cookie_name="auth", cookie_max_age=3600)
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=lambda: JWTStrategy(secret="SECRET", lifetime_seconds=3600),
)

fastapi_users = FastAPIUsers[UserCreate, UserDB, UserUpdate](
    get_user_db, [auth_backend]
)

current_active_user = fastapi_users.current_user(active=True)
