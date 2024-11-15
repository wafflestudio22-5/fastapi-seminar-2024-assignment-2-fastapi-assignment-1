from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from wapang.common.errors import WapangHttpException


class OrderNotFoundError(WapangHttpException):
    def __init__(self):
        super().__init__(HTTP_404_NOT_FOUND, "Order not found")

class AlreadyCanceledError(WapangHttpException):
    def __init__(self):
        super().__init__(HTTP_400_BAD_REQUEST, "Order already canceled")