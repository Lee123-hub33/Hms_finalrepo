"""Drug and supplies stock control."""

import enum
from sqlalchemy import CheckConstraint, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ItemCategoryEnum(str, enum.Enum):
    drug     = "Drug"
    supplies = "Supplies"


class Inventory(Base):
    __tablename__ = "inventory"
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="ck_inventory_quantity_non_negative"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    item_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    category: Mapped[ItemCategoryEnum] = mapped_column(Enum(ItemCategoryEnum), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    reorder_level: Mapped[int] = mapped_column(Integer, default=10, nullable=False)

    @property
    def needs_reorder(self) -> bool:
        return self.quantity <= self.reorder_level

    def __repr__(self) -> str:
        return f"<Inventory item={self.item_name!r} qty={self.quantity}>"