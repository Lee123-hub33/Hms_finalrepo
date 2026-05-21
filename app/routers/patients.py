"""Patient registration and lookup."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import PatientCreate, PatientOut
from app.schemas import PatientUpdate

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("", response_model=PatientOut, status_code=201)
def register_patient(data: PatientCreate, db: Session = Depends(get_db)):
    """Register a new patient."""
    return crud.create_patient(db, data)


@router.get("", response_model=List[PatientOut])
def list_patients(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """List all patients with pagination."""
    return crud.get_patients(db, skip=skip, limit=limit)


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Fetch a single patient — returns 404 if not found."""
    return crud.get_patient_by_id(db, patient_id)


@router.patch("/{patient_id}", response_model=PatientOut)
def update_patient(patient_id: int, data: PatientUpdate, db: Session = Depends(get_db)):
    return crud.update_patient(db, patient_id, data.model_dump(exclude_none=True))