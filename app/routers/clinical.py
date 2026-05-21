"""Vitals, consultation, ANC, and procedure endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.auth import check_role
from app.database import get_db
from app.schemas import (
    ANCCreate, ANCOut, ConsultationCreate, ConsultationOut,
    VitalsOut, VitalsUpdate,
)

router = APIRouter(prefix="/clinical", tags=["Clinical"])


@router.patch("/vitals", response_model=VitalsOut)
def attach_vitals(
    data: VitalsUpdate,
    db: Session = Depends(get_db),
    _=Depends(check_role(["Doctor", "Nurse"])),
):
    """Record or update vitals for an existing Encounter."""
    return crud.upsert_vitals(db, data)


@router.post("/consultation", response_model=ConsultationOut, status_code=201)
def create_consultation(
    data: ConsultationCreate,
    db: Session = Depends(get_db),
    _=Depends(check_role(["Doctor"])),
):
    """Doctors only — attach diagnosis and clinical notes to an Encounter."""
    return crud.create_consultation(db, data)


@router.post("/anc", response_model=ANCOut, status_code=201)
def create_anc(
    data: ANCCreate,
    db: Session = Depends(get_db),
    _=Depends(check_role(["Doctor", "Nurse"])),
):
    """Record ANC details for an Encounter."""
    return crud.create_anc(db, data)


@router.get("/vitals/{encounter_id}", response_model=VitalsOut)
def get_vitals(encounter_id: int, db: Session = Depends(get_db), _=Depends(check_role(["Doctor", "Nurse"]))):
    return crud.get_vitals_by_encounter(db, encounter_id)