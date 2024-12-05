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

class InvalidUsernameOrPasswordError(WapangHttpException):
    def __init__(self) -> None:
        super().__init__(401, "Invalid username or password")

class ExpiredSignatureError(WapangHttpException):
    def __init__(self) -> None:
        super().__init__(401, "Token expired")

class InvalidTokenError(WapangHttpException):
    def __init__(self) -> None:
        super().__init__(401, "Invalid token")

class BlockedTokenError(WapangHttpException):
    def __init__(self) -> None:
        super().__init__(401, "Blocked token")