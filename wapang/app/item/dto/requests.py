from pydantic import BaseModel


class ItemCreateRequest(BaseModel):
    item_name: str
    price: int
    stock: int

class ItemUpdateRequest(BaseModel):
    item_name: str | None = None
    price: int | None = None
    stock: int | None = None
