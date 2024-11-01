from typing import Annotated
from pydantic import AfterValidator, BaseModel, EmailStr

from wapang.common.utils import validate_phone_number


class StoreCreateRequest(BaseModel):
    store_name: str
    address: str | None = None
    email: EmailStr | None = None
    phone_number: Annotated[str | None, AfterValidator(validate_phone_number)] = None
