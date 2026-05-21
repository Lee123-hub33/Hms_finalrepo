from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud
from app.auth import check_role
from app.database import get_db
from app.schemas import WardCreate, WardOut

router = APIRouter(prefix="/wards", tags=["Wards"])

@router.post("", response_model=WardOut, status_code=201, dependencies=[Depends(check_role(["Admin"]))])
def create_ward(
    data: WardCreate,
    db: Session = Depends(get_db),
):
    """Create a new ward."""
    try:
        return crud.create_ward(db, data)
    except IntegrityError as exc:
        db.rollback()
        if "wards_ward_name_key" in str(exc.orig) or "duplicate key value violates unique constraint" in str(exc.orig):
            raise HTTPException(status_code=409, detail="Ward name already exists.")
        raise HTTPException(status_code=400, detail="Could not create ward.")

@router.get("", response_model=List[WardOut], dependencies=[Depends(check_role(["Admin", "Doctor", "Nurse"]))])
def list_wards(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
):
    """List all wards."""
    return crud.get_wards(db, skip=skip, limit=limit)
