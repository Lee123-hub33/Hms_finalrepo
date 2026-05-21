"""Inpatient ward registry."""

from sqlalchemy import CheckConstraint, Column, Integer, String

from app.database import Base


class Ward(Base):
    __tablename__ = "wards"
    __table_args__ = (
        CheckConstraint("current_occupancy >= 0", name="ck_ward_occupancy_non_negative"),
        CheckConstraint("current_occupancy <= capacity", name="ck_ward_occupancy_capacity"),
    )

    id                = Column(Integer, primary_key=True, index=True)
    ward_name         = Column(String(255), nullable=False, unique=True)
    capacity          = Column(Integer, nullable=False)
    current_occupancy = Column(Integer, default=0, nullable=False)

    def __repr__(self) -> str:
        return f"<Ward id={self.id} name={self.ward_name!r}>"