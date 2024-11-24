from typing import Annotated

from fastapi import Depends
from wapang.app.store.dto.responses import StoreDetailResponse
from wapang.app.store.errors import (
    AlreadyHasStoreError,
    StoreAlreadyExistsError,
    StoreNotFoundError,
)
from wapang.app.store.store import StoreStore
from wapang.app.user.models import User
from wapang.common.errors import MissingRequiredFieldError


class StoreService:
    def __init__(self, store_store: Annotated[StoreStore, Depends()]):
        self.store_store = store_store

    def create_store(
        self,
        user: User,
        name: str,
        address: str | None,
        email: str | None,
        phone_number: str | None,
    ) -> StoreDetailResponse:
        address = address or user.address
        email = email or user.email
        phone_number = phone_number or user.phone_number
        if not name or not address or not email or not phone_number:
            raise MissingRequiredFieldError()

        self.raise_if_store_exists(user.id, name, email, phone_number)
        store = self.store_store.create_store(
            name=name,
            address=address,
            email=email,
            phone_number=phone_number,
            owner_id=user.id,
        )
        return StoreDetailResponse.model_validate(store, from_attributes=True)

    def get_store_by_id(self, store_id: int) -> StoreDetailResponse:
        store = self.store_store.get_store_by_id(store_id)
        if store is None:
            raise StoreNotFoundError()
        return StoreDetailResponse.model_validate(store, from_attributes=True)

    def raise_if_store_exists(
        self, owner_id: int, name: str, email: str, phone_number: str
    ) -> None:
        store = self.store_store.get_store(owner_id, name, email, phone_number)
        if store is not None:
            if store.owner_id == owner_id:
                raise AlreadyHasStoreError()
            if store.name == name:
                raise StoreAlreadyExistsError("Store")
            if store.email == email:
                raise StoreAlreadyExistsError("Email")
            if store.phone_number == phone_number:
                raise StoreAlreadyExistsError("Phone number")
