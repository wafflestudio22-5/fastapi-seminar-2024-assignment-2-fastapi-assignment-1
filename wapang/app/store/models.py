from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from wapang.database.common import Base, intpk

if TYPE_CHECKING:
    from wapang.app.user.models import User
    from wapang.app.item.models import Item


class Store(Base):
    __tablename__ = "store"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    address: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(20))
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    owner: Mapped["User"] = relationship("User", back_populates="stores")
    items: Mapped[list["Item"]] = relationship("Item", back_populates="store")
