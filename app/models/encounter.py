"""
Central visit registry — every clinical action anchors to an Encounter ID.

Fix [03]: Removed 'inpatient' from VisitTypeEnum (belongs in PatientStatusEnum only).
Fix [04]: Added created_at — filtering by date in reporting_service was broken without it.
"""

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class VisitTypeEnum(str, enum.Enum):
    opd       = "OPD"
    anc       = "ANC"
    emergency = "Emergency"


class PatientStatusEnum(str, enum.Enum):
    pending    = "Pending"
    inpatient  = "Inpatient"
    outpatient = "Outpatient"


class TriageLevelEnum(str, enum.Enum):
    emergency = "Emergency"
    urgent = "Urgent"
    normal = "Normal"


class Encounter(Base):
    __tablename__ = "encounters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    staff_id: Mapped[int] = mapped_column(Integer, ForeignKey("staff.id"), nullable=False, index=True)
    visit_type: Mapped[VisitTypeEnum] = mapped_column(Enum(VisitTypeEnum), nullable=False)
    patient_status: Mapped[PatientStatusEnum] = mapped_column(Enum(PatientStatusEnum), nullable=False, default=PatientStatusEnum.pending)
    triage_level: Mapped[TriageLevelEnum] = mapped_column(Enum(TriageLevelEnum), nullable=False, default=TriageLevelEnum.normal)
    ward_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("wards.id"), nullable=True)
    bed_number: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    discharged: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    discharge_notes: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    discharged_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<Encounter id={self.id} patient_id={self.patient_id} visit_type={self.visit_type}>"