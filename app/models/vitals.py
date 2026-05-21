"""Patient vitals recorded per Encounter."""

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class Vitals(Base):
    __tablename__ = "vitals"

    id            = Column(Integer, primary_key=True, index=True)
    encounter_id  = Column(Integer, ForeignKey("encounters.id"), nullable=False, unique=True, index=True)
    temperature   = Column(Float)              # °C
    blood_pressure = Column(String(20))        # e.g. "120/80 mmHg"
    weight        = Column(Float)              # kg
    height        = Column(Float)              # cm
    muac          = Column(Float)              # Mid-Upper Arm Circumference, cm
    recorded_at   = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Vitals encounter_id={self.encounter_id} temp={self.temperature}>"