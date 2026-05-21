"""Clinician registry (legacy table kept for compatibility)."""

from sqlalchemy import Column, Integer, String

from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id             = Column(Integer, primary_key=True, index=True)
    name           = Column(String(255), nullable=False)
    specialization = Column(String(255))
    license_number = Column(String(100), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Doctor id={self.id} name={self.name!r}>"