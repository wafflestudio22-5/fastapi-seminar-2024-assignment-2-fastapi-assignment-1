from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, ForeignKey, Enum, Integer
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wapang.app.order.enums import OrderStatus
from wapang.database.common import Base, intpk

if TYPE_CHECKING:
    from wapang.app.item.models import Item
    from wapang.app.user.models import User


class OrderItem(Base):
    __tablename__ = "order_item_list"

    order_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("order.id"), nullable=False, primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("item.id"), nullable=False, primary_key=True
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)


class Order(AsyncAttrs, Base):
    __tablename__ = "order"

    id: Mapped[intpk] = mapped_column(BigInteger, primary_key=True)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False)
    orderer_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    orderer: Mapped["User"] = relationship("User", back_populates="orders")
    order_items: Mapped[list[OrderItem]] = relationship(OrderItem)
    items: Mapped[list["Item"]] = relationship(
        secondary="order_item_list", back_populates="orders"
    )
