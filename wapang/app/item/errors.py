from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)

from wapang.common.errors import WapangHttpException

class ItemNotFoundError(WapangHttpException):
    def __init__(self) -> None:
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail="Item not found")