from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from wapang.common.errors import WapangHttpException


class StoreAlreadyExistsError(WapangHttpException):
    def __init__(self, field: str):
        super().__init__(HTTP_409_CONFLICT, f"{field} already exists")

class AlreadyHasStoreError(WapangHttpException):
    def __init__(self):
        super().__init__(HTTP_403_FORBIDDEN, "User already has a store")

class StoreNotFoundError(WapangHttpException):
    def __init__(self):
        super().__init__(HTTP_404_NOT_FOUND, "Store not found")
