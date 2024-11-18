from wapang.common.errors import WapangHttpException


class ItemNotFoundError(WapangHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Item not found")
