from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_409_CONFLICT,
)

from wapang.common.errors import WapangHttpException


class EmailAlreadyExistsError(WapangHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_409_CONFLICT, "Email already exists")


class UsernameAlreadyExistsError(WapangHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_409_CONFLICT, "Username already exists")


class UserUnsignedError(WapangHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_401_UNAUTHORIZED, "User is not signed in")


class PermissionDeniedError(WapangHttpException):
    def __init__(self) -> None:
        super().__init__(HTTP_403_FORBIDDEN, "User does not have permission")
