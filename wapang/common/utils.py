from contextvars import ContextVar
from uuid import uuid4
from wapang.common.errors import InvalidFieldFormatError


def validate_phone_number(value: str | None) -> str | None:
    if value is None:
        return None
    if not value.startswith("010") or not len(value) == 11 or not value.isdigit():
        raise InvalidFieldFormatError()
    return value

request_id: ContextVar[str] = ContextVar("request_id")

def get_request_id() -> str:
    if request_id.get(None) is None:
        request_id.set(str(uuid4()))
    return request_id.get()
