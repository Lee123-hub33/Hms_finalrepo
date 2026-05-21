"""
Patient demographics.

Fix [10]: Added created_at — required for date-scoped MoH reports.
"""

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(255), nullable=False)
    age        = Column(Integer, nullable=False)
    gender     = Column(String(10), nullable=False)       # Male / Female / Other
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Patient id={self.id} name={self.name!r} age={self.age}>"