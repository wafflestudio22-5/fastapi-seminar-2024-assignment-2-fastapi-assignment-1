from typing import TYPE_CHECKING
from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wapang.database.common import Base, intpk

if TYPE_CHECKING:
    from wapang.app.store.models import Store
    from wapang.app.order.models import Order

class Item(Base):
    __tablename__ = "item"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    price: Mapped[int] = mapped_column(BigInteger)
    stock: Mapped[int] = mapped_column(Integer)
    store_id: Mapped[int] = mapped_column(ForeignKey("store.id"))

    store: Mapped["Store"] = relationship("Store", back_populates="items")
    orders: Mapped[list["Order"]] = relationship(secondary='order_item_list', back_populates="items")
