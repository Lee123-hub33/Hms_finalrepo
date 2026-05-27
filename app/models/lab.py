"""
Laboratory request and results.

Fix [07]: status default changed from string "Pending" to LabStatusEnum.pending.
"""

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class LabStatusEnum(str, enum.Enum):
    pending   = "Pending"
    completed = "Completed"


class LabRequest(Base):
    __tablename__ = "lab_requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    encounter_id: Mapped[int] = mapped_column(Integer, ForeignKey("encounters.id"), nullable=False, index=True)
    test_requested: Mapped[str] = mapped_column(String(255), nullable=False)
    results: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    technician_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[LabStatusEnum] = mapped_column(Enum(LabStatusEnum), nullable=False, default=LabStatusEnum.pending)
    requested_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<LabRequest id={self.id} test={self.test_requested!r} status={self.status}>"