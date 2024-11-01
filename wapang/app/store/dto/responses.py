from pydantic import BaseModel, Field


class StoreCreateResponse(BaseModel):
    id: int
    name: str = Field(serialization_alias="store_name")
    address: str
    email: str
    phone_number: str
