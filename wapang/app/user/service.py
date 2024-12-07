from typing import Annotated

from fastapi import Depends
from wapang.app.user.models import User
from wapang.app.user.store import UserStore


class UserService:
    def __init__(self, user_store: Annotated[UserStore, Depends()]) -> None:
        self.user_store = user_store

    async def add_user(self, username: str, password: str, email: str):
        await self.user_store.add_user(username=username, password=password, email=email)

    async def get_user_by_username(self, username: str) -> User | None:
        return await self.user_store.get_user_by_username(username)

    async def update_user(
        self,
        username: str,
        email: str | None,
        address: str | None,
        phone_number: str | None,
    ) -> User:
        return await self.user_store.update_user(username, email, address, phone_number)
