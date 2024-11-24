from typing import Annotated
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from wapang.app.store.errors import AlreadyHasStoreError, StoreAlreadyExistsError
from wapang.app.store.models import Store
from wapang.database.connection import get_db_session


# 이렇게 보니까 좀 이상하네요 ㅎㅎ;
# 보통 ~Store보다 ~Repository라는 이름을 더 많이 쓰긴 합니다.
class StoreStore:
    def __init__(self, session: Annotated[Session, Depends(get_db_session)]):
        self.session = session

    def create_store(
        self, name: str, address: str, email: str, phone_number: str, owner_id: int
    ) -> Store:
        store = Store(
            name=name,
            address=address,
            email=email,
            phone_number=phone_number,
            owner_id=owner_id,
        )
        self.session.add(store)
        self.session.flush()
        return store

    def get_store_by_id(self, store_id: int) -> Store | None:
        get_store_query = select(Store).filter(Store.id == store_id)
        store = self.session.scalar(get_store_query)
        return store

    def get_store_of_user(self, user_id: int) -> Store | None:
        get_store_query = select(Store).filter(Store.owner_id == user_id)
        store = self.session.scalar(get_store_query)
        return store

    def get_store_by_name(self, name: str) -> Store | None:
        get_store_query = select(Store).filter(Store.name == name)
        store = self.session.scalar(get_store_query)
        return store

    def get_store(
        self, owner_id: int, name: str, email: str, phone_number: str
    ) -> Store | None:
        get_store_query = select(Store).filter(
            (Store.owner_id == owner_id)
            | (Store.name == name)
            | (Store.email == email)
            | (Store.phone_number == phone_number)
        )
        return self.session.scalar(get_store_query)
