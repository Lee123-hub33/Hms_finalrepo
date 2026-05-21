"""Clinical procedure performed during an Encounter."""

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class Procedure(Base):
    __tablename__ = "procedures"

    id             = Column(Integer, primary_key=True, index=True)
    encounter_id   = Column(Integer, ForeignKey("encounters.id"), nullable=False, index=True)
    procedure_name = Column(String(255), nullable=False)
    description    = Column(Text)
    cost           = Column(Float, default=0.0, nullable=False)
    performed_at   = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Procedure id={self.id} name={self.procedure_name!r} cost={self.cost}>"