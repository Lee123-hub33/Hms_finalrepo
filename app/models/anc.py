"""
Antenatal Care record.

Fix [06]: Added missing Date import from sqlalchemy.
"""

from sqlalchemy import Column, Date, ForeignKey, Integer, String

from app.database import Base


class ANC(Base):
    __tablename__ = "anc"

    id           = Column(Integer, primary_key=True, index=True)
    encounter_id = Column(Integer, ForeignKey("encounters.id"), nullable=False, unique=True, index=True)
    anc_number   = Column(String(50), unique=True, nullable=False)
    gravida      = Column(Integer, nullable=False)   # Total pregnancies including current
    parity       = Column(Integer, nullable=False)   # Pregnancies ≥ 20 weeks
    lmp          = Column(Date, nullable=True)       # Last Menstrual Period
    edd          = Column(Date, nullable=True)       # Estimated Date of Delivery

    def __repr__(self) -> str:
        return f"<ANC id={self.id} anc_number={self.anc_number!r}>"