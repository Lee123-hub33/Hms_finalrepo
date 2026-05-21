from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.auth import check_role
from app.database import get_db
from app.schemas import ProcedureCreate, ProcedureOut

router = APIRouter(prefix="/procedures", tags=["Procedures"])

@router.post("", response_model=ProcedureOut, status_code=201, dependencies=[Depends(check_role(["Doctor", "Nurse"]))])
def create_procedure(
    data: ProcedureCreate,
    db: Session = Depends(get_db),
):
    """Record a clinical procedure for an encounter."""
    return crud.create_procedure(db, data)
