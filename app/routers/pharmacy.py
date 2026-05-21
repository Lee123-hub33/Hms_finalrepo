from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.auth import check_role
from app.database import get_db
from app.schemas import PrescriptionCreate, PrescriptionOut

router = APIRouter(prefix="/pharmacy", tags=["Pharmacy"])

@router.post("/prescription", response_model=PrescriptionOut, status_code=201, dependencies=[Depends(check_role(["Doctor"]))])
def create_prescription(
    data: PrescriptionCreate,
    db: Session = Depends(get_db),
):
    """Create a prescription for an encounter."""
    return crud.create_prescription(db, data)

@router.patch("/prescription/{prescription_id}/dispense", response_model=PrescriptionOut, dependencies=[Depends(check_role(["Pharmacy"]))])
def dispense_prescription(
    prescription_id: int,
    db: Session = Depends(get_db),
):
    """Mark a prescription as dispensed."""
    return crud.dispense_prescription(db, prescription_id)
