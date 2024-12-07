from datetime import datetime
from functools import cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from wapang.app.user.errors import (
    EmailAlreadyExistsError,
    UserUnsignedError,
    UsernameAlreadyExistsError,
)
from wapang.app.user.models import BlockedToken, User
from wapang.database.annotation import transactional
from wapang.database.connection import SESSION


class UserStore:
    @transactional
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

    @transactional
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

    @transactional
    async def block_token(self, token_id: str, expired_at: datetime) -> None:
        blocked_token = BlockedToken(token_id=token_id, expired_at=expired_at)
        SESSION.add(blocked_token)

    async def is_token_blocked(self, token_id: int) -> bool:
        return (
            await SESSION.scalar(
                select(BlockedToken).where(BlockedToken.token_id == token_id)
            )
            is not None
        )
