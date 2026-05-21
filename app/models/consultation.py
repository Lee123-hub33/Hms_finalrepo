"""Clinical consultation note — Doctors only."""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class Consultation(Base):
    __tablename__ = "consultations"

    id              = Column(Integer, primary_key=True, index=True)
    encounter_id    = Column(Integer, ForeignKey("encounters.id"), nullable=False, index=True)
    chief_complaint = Column(Text)
    clinical_notes  = Column(Text)
    diagnosis       = Column(String(500), nullable=False)   # ICD-10 code or free text
    created_at      = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Consultation encounter_id={self.encounter_id} dx={self.diagnosis!r}>"