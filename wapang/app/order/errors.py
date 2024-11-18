from wapang.common.errors import WapangHttpException


class OrderNotFoundError(WapangHttpException):
    def __init__(self):
        super().__init__(404, "Order not found")


class AlreadyCanceledError(WapangHttpException):
    def __init__(self):
        super().__init__(400, "Order already canceled")

class NotEnoughStockError(WapangHttpException):
    def __init__(self):
        super().__init__(400, "Not enough stock")