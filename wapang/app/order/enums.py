from enum import StrEnum


class OrderStatus(StrEnum):
    CANCELED = "CANCELED"
    ORDERED = "ORDERED"
    COMPLETE = "COMPLETE"
