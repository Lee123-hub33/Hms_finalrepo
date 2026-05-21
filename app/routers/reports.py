"""MoH reporting endpoints."""

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth import check_role
from app.database import get_db
from app.schemas import ANCReportRow, DailyRegistryRow, MOH705Report
from app.services import reporting_service

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/daily-registry", response_model=List[DailyRegistryRow])
def daily_registry(
    target_date: Optional[date] = Query(default=None, description="Defaults to today"),
    db: Session = Depends(get_db),
    _=Depends(check_role(["Admin", "Doctor", "Nurse"])),
):
    """Full encounter list for the day — used as the patient register."""
    return reporting_service.generate_daily_registry(db, target_date)


@router.get("/moh-summary", response_model=MOH705Report)
def moh_summary(
    target_date: Optional[date] = Query(default=None, description="Defaults to today"),
    db: Session = Depends(get_db),
    _=Depends(check_role(["Admin", "Doctor"])),
):
    """MoH 705 — Under 5 / Over 5 attendance counts grouped by diagnosis."""
    return reporting_service.generate_moh_705(db, target_date)


@router.get("/anc", response_model=List[ANCReportRow])
def anc_report(
    month: int = Query(..., ge=1, le=12, description="1 = January"),
    year:  int = Query(..., ge=2000),
    db: Session = Depends(get_db),
    _=Depends(check_role(["Admin", "Doctor", "Nurse"])),
):
    """MoH ANC monthly register."""
    return reporting_service.generate_anc_report(db, month, year)