"""
Operational staff with role-based access.

Fix [05]: UniqueConstraint on user_id — one staff profile per user account.
"""

import enum
from typing import Optional

from sqlalchemy import Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class RoleEnum(str, enum.Enum):
    doctor    = "Doctor"
    nurse     = "Nurse"
    admin     = "Admin"
    lab       = "Lab"
    pharmacy  = "Pharmacy"
    accounts  = "Accounts"


class Staff(Base):
    __tablename__ = "staff"
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_staff_user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False)
    department: Mapped[Optional[str]] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<Staff id={self.id} name={self.name!r} role={self.role}>"