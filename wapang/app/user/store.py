from functools import cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from wapang.app.user.errors import EmailAlreadyExistsError, UserUnsignedError, UsernameAlreadyExistsError
from wapang.app.user.models import User
from wapang.database.connection import SESSION


class UserStore:
    async def add_user(self, username: str, password: str, email: str) -> User:
        if await self.get_user_by_username(username):
            raise UsernameAlreadyExistsError()

        if await self.get_user_by_email(email):
            raise EmailAlreadyExistsError()

        user = User(username=username, password=password, email=email)
        SESSION.add(user)
        return user

    async def get_user_by_username(self, username: str) -> User | None:
        return await SESSION.scalar(select(User).where(User.username == username))

    async def get_user_by_email(self, email: str) -> User | None:
        return await SESSION.scalar(select(User).where(User.email == email))

    async def update_user(
        self,
        username: str,
        email: str | None,
        address: str | None,
        phone_number: str | None,
    ) -> User:
        user = await self.get_user_by_username(username)
        if user is None:
            raise UserUnsignedError()

        if email is not None:
            if self.get_user_by_email(email):
                raise EmailAlreadyExistsError()
            user.email = email

        if address is not None:
            user.address = address

        if phone_number is not None:
            user.phone_number = phone_number

        return user
