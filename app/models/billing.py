"""
Patient billing per Encounter.

Fix [09]: status default changed from string "Unpaid" to BillingStatusEnum.unpaid.
"""

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class BillingStatusEnum(str, enum.Enum):
    paid   = "Paid"
    unpaid = "Unpaid"


class Billing(Base):
    __tablename__ = "billing"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    encounter_id: Mapped[int] = mapped_column(Integer, ForeignKey("encounters.id"), nullable=False, index=True)
    service_type: Mapped[str] = mapped_column(String(255), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[BillingStatusEnum] = mapped_column(Enum(BillingStatusEnum), nullable=False, default=BillingStatusEnum.unpaid)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<Billing id={self.id} amount={self.amount} status={self.status}>"