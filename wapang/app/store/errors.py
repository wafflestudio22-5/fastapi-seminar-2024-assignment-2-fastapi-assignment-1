from wapang.common.errors import WapangHttpException


class StoreAlreadyExistsError(WapangHttpException):
    def __init__(self, field: str):
        super().__init__(409, f"{field} already exists")


class AlreadyHasStoreError(WapangHttpException):
    def __init__(self):
        super().__init__(403, "User already has a store")


class StoreNotFoundError(WapangHttpException):
    def __init__(self):
        super().__init__(404, "Store not found")
