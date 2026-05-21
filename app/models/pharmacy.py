"""
Prescription and dispensing.

Fix [08]: status default changed from string "Pending" to PharmacyStatusEnum.pending.
"""

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class PharmacyStatusEnum(str, enum.Enum):
    pending   = "Pending"
    dispensed = "Dispensed"


class Prescription(Base):
    __tablename__ = "prescriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    encounter_id: Mapped[int] = mapped_column(Integer, ForeignKey("encounters.id"), nullable=False, index=True)
    prescription_details: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[PharmacyStatusEnum] = mapped_column(Enum(PharmacyStatusEnum), nullable=False, default=PharmacyStatusEnum.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    dispensed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<Prescription id={self.id} encounter_id={self.encounter_id} status={self.status}>"