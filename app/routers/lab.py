"""Lab request and result management — Lab Techs only."""

from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.auth import check_role
from app.database import get_db
from app.models.lab import LabStatusEnum
from app.schemas import LabOut, LabRequestCreate, LabResultUpdate

router = APIRouter(prefix="/lab", tags=["Laboratory"])


@router.get("", response_model=List[LabOut])
def list_lab_requests(
    status: Optional[LabStatusEnum] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _=Depends(check_role(["Doctor", "Lab"])),
):
    return crud.get_all_lab_requests(db, skip=skip, limit=limit, status=status)


@router.post("", response_model=LabOut, status_code=201)
def request_lab(
    data: LabRequestCreate,
    db: Session = Depends(get_db),
    _=Depends(check_role(["Doctor", "Lab"])),
):
    return crud.create_lab_request(db, data)


@router.patch("/{lab_id}/results", response_model=LabOut)
def enter_results(
    lab_id: int,
    data: LabResultUpdate,
    db: Session = Depends(get_db),
    _=Depends(check_role(["Lab"])),
):
    """Lab Techs only — record results and mark request as Completed."""
    return crud.complete_lab_request(db, lab_id, data.results, data.technician_notes)


@router.get("/encounter/{encounter_id}", response_model=List[LabOut])
def list_lab_by_encounter(encounter_id: int, db: Session = Depends(get_db), _=Depends(check_role(["Doctor", "Lab"]))):
    return crud.get_lab_requests_by_encounter(db, encounter_id)