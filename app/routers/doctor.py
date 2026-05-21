from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.auth import check_role
from app.database import get_db
from app.schemas import DoctorCreate, DoctorOut

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.post("", response_model=DoctorOut, status_code=201, dependencies=[Depends(check_role(["Admin"]))])
def register_doctor(
    data: DoctorCreate,
    db: Session = Depends(get_db),
):
    """Register a new doctor."""
    return crud.create_doctor(db, data)

@router.get("", response_model=List[DoctorOut])
def list_doctors(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """List all doctors."""
    return crud.get_doctors(db, skip=skip, limit=limit)
