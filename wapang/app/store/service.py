from typing import Annotated

from fastapi import Depends
from wapang.app.store.dto.responses import StoreDetailResponse
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
        return StoreDetailResponse.model_validate(store, from_attributes=True)
