"""Billing management — Admin and Accounts roles only."""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.auth import check_role
from app.database import get_db
from app.schemas import BillingCreate, BillingOut

router = APIRouter(prefix="/billing", tags=["Billing"])

_BILLING_ROLES = ["Admin", "Accounts"]


@router.post("", response_model=BillingOut, status_code=201)
def create_bill(
    data: BillingCreate,
    db: Session = Depends(get_db),
    _=Depends(check_role(_BILLING_ROLES)),
):
    return crud.create_bill(db, data)


@router.patch("/{bill_id}/pay", response_model=BillingOut)
def mark_paid(
    bill_id: int,
    db: Session = Depends(get_db),
    _=Depends(check_role(_BILLING_ROLES)),
):
    return crud.mark_bill_paid(db, bill_id)


@router.get("/encounter/{encounter_id}", response_model=List[BillingOut])
def billing_by_encounter(encounter_id: int, db: Session = Depends(get_db), _=Depends(check_role(_BILLING_ROLES))):
    return crud.get_billing_by_encounter(db, encounter_id)