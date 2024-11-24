from typing import Annotated
from pydantic import AfterValidator, BaseModel, EmailStr, field_validator

from wapang.common.errors import InvalidFieldFormatError
from wapang.common.utils import validate_phone_number


class StoreCreateRequest(BaseModel):
    store_name: str
    address: str | None = None
    email: EmailStr | None = None
    phone_number: Annotated[str | None, AfterValidator(validate_phone_number)] = None

    @field_validator("store_name")
    def validate_store_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if len(value) < 3 or len(value) > 20:
            raise InvalidFieldFormatError()
        return value
