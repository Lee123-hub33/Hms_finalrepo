"""Encounter (check-in) management."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.auth import get_current_staff
from app.database import get_db
from app.models.staff import Staff
from app.schemas import EncounterCreate, EncounterOut

router = APIRouter(prefix="/registry", tags=["Registry"])


@router.post("/check-in", response_model=EncounterOut, status_code=201)
def check_in(
    data: EncounterCreate,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    """
    Create an Encounter — the anchor ID for all clinical data on this visit.
    Fix [17]: visit_type and patient_status now validated by Pydantic enum fields.
    """
    return crud.create_encounter(db, data, staff_id=current_staff.id)


@router.get("/patient/{patient_id}", response_model=List[EncounterOut])
def get_patient_history(
    patient_id: int,
    db: Session = Depends(get_db),
    current_staff: Staff = Depends(get_current_staff),
):
    """Return visit history (encounters) for a patient."""
    return crud.get_encounters_by_patient(db, patient_id)


@router.get("/{encounter_id}", response_model=EncounterOut)
def get_encounter(encounter_id: int, db: Session = Depends(get_db), current_staff: Staff = Depends(get_current_staff)):
    """Fetch a single encounter by id."""
    return crud.get_encounter_or_404(db, encounter_id)


@router.post("/{encounter_id}/discharge", response_model=EncounterOut)
def discharge(encounter_id: int, db: Session = Depends(get_db), current_staff: Staff = Depends(get_current_staff)):
    """Mark an encounter as discharged."""
    return crud.discharge_encounter(db, encounter_id)


@router.post("/{encounter_id}/assign-bed", response_model=EncounterOut)
def assign_bed(encounter_id: int, bed_number: str, db: Session = Depends(get_db), current_staff: Staff = Depends(get_current_staff)):
    """Assign a bed number to an encounter (inpatient admissions)."""
    return crud.assign_bed(db, encounter_id, bed_number)