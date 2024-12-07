from functools import wraps
import re
from typing import Annotated, Callable, TypeVar
from pydantic import BaseModel, EmailStr
from pydantic.functional_validators import AfterValidator

from wapang.common.errors import InvalidFieldFormatError
from wapang.common.utils import validate_phone_number


USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")


def validate_username(value: str | None) -> str | None:
    if value is None:
        return value
    if not re.match(USERNAME_PATTERN, value):
        raise InvalidFieldFormatError()
    return value


def validate_password(value: str | None) -> str | None:
    if value is None:
        return value
    if len(value) < 8 or len(value) > 20:
        raise InvalidFieldFormatError()

    contains_uppercase = False
    contains_lowercase = False
    contains_digit = False
    contains_special = False

    for char in value:
        if char.isupper():
            contains_uppercase = True
        elif char.islower():
            contains_lowercase = True
        elif char.isdigit():
            contains_digit = True
        else:
            contains_special = True

    constraints_cardinality = sum(
        [contains_uppercase, contains_lowercase, contains_digit, contains_special]
    )
    if constraints_cardinality < 2:
        raise InvalidFieldFormatError()

    return value


def validate_address(value: str) -> str:
    if len(value) > 100:
        raise InvalidFieldFormatError()
    return value


class UserSignupRequest(BaseModel):
    username: Annotated[str, AfterValidator(validate_username)]
    # TODO 과제1 에서는 연습을 위해 외부 라이브러리를 사용하지 말라고 말씀드렸지만,
    # 실전에서는 당연히 좋은 라이브러리가 있다면 적절히 사용하는 것이 좋습니다.
    # 개발자라면 누구나 알법한 명언이 있죠. "바퀴를 재발명하지 마세요."
    email: EmailStr
    password: Annotated[str, AfterValidator(validate_password)]


class UserUpdateRequest(BaseModel):
    email: EmailStr | None = None
    address: Annotated[str | None, AfterValidator(validate_address)] = None
    phone_number: Annotated[str | None, AfterValidator(validate_phone_number)] = None

class UserSigninRequest(BaseModel):
    username: str
    password: str
