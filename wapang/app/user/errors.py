from wapang.common.errors import WapangHttpException


class EmailAlreadyExistsError(WapangHttpException):
    def __init__(self) -> None:
        super().__init__(409, "Email already exists")


class UsernameAlreadyExistsError(WapangHttpException):
    def __init__(self) -> None:
        super().__init__(409, "Username already exists")


class UserUnsignedError(WapangHttpException):
    def __init__(self) -> None:
        super().__init__(401, "User is not signed in")


class PermissionDeniedError(WapangHttpException):
    def __init__(self) -> None:
        super().__init__(403, "User does not have permission")
