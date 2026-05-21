from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.auth import check_role
from app.database import get_db
from app.schemas import StaffCreate, StaffOut

router = APIRouter(prefix="/staff", tags=["Staff"])

@router.post("", response_model=StaffOut, status_code=201, dependencies=[Depends(check_role(["Admin"]))])
def create_staff_member(
    data: StaffCreate,
    db: Session = Depends(get_db),
):
    """Create a new staff member."""
    return crud.create_staff(db, data)

@router.get("", response_model=List[StaffOut], dependencies=[Depends(check_role(["Admin"]))])
def list_staff(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
):
    """List all staff members."""
    return crud.get_staff(db, skip=skip, limit=limit)
