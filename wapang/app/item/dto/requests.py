from typing import Annotated
from pydantic import AfterValidator, BaseModel

from wapang.common.errors import InvalidFieldFormatError


def price_should_be_greater_than_zero(price: int | None) -> int | None:
    if price is None:
        return None
    if price <= 0:
        raise InvalidFieldFormatError()
    return price


def stock_should_be_greater_than_or_equal_to_zero(stock: int | None) -> int | None:
    if stock is None:
        return None
    if stock < 0:
        raise InvalidFieldFormatError()
    return stock


def item_name_between_2_and_50(item_name: str | None) -> str | None:
    if item_name is None:
        return None
    if len(item_name) < 2 or len(item_name) > 50:
        raise InvalidFieldFormatError()
    return item_name


class ItemCreateRequest(BaseModel):
    item_name: Annotated[str, AfterValidator(item_name_between_2_and_50)]
    price: Annotated[int, AfterValidator(price_should_be_greater_than_zero)]
    stock: Annotated[int, AfterValidator(stock_should_be_greater_than_or_equal_to_zero)]


class ItemUpdateRequest(BaseModel):
    item_name: Annotated[str | None, AfterValidator(item_name_between_2_and_50)] = None
    price: Annotated[int | None, AfterValidator(price_should_be_greater_than_zero)] = (
        None
    )
    stock: Annotated[
        int | None, AfterValidator(stock_should_be_greater_than_or_equal_to_zero)
    ] = None
