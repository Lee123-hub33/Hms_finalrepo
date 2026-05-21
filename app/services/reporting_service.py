"""
MoH reporting functions.

Fix [21]: Replaced r.ANC tuple access with explicit aliased() — SQLAlchemy 2.x safe.
Fix [22]: generate_moh_705 now groups into age BANDS (< 5 / >= 5) before aggregating,
          not by individual age integer values.
"""

from datetime import date
from typing import Any, Dict, List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.anc import ANC
from app.models.consultation import Consultation
from app.models.encounter import Encounter
from app.models.patient import Patient


def generate_daily_registry(
    db: Session,
    target_date: Optional[date] = None,
) -> List[Dict[str, Any]]:
    """
    Full patient registry for the given date.
    Returns: encounter_id, patient name, age, sex, diagnosis, visit type, time.
    """
    target_date = target_date or date.today()

    rows = (
        db.query(
            Encounter.id.label("encounter_id"),
            Encounter.visit_type,
            Encounter.created_at,
            Patient.name.label("patient_name"),
            Patient.age,
            Patient.gender,
            Consultation.diagnosis,
        )
        .join(Patient, Patient.id == Encounter.patient_id)
        .outerjoin(Consultation, Consultation.encounter_id == Encounter.id)
        .filter(func.date(Encounter.created_at) == target_date)
        .order_by(Encounter.created_at)
        .all()
    )

    return [
        {
            "encounter_id": r.encounter_id,
            "patient_name": r.patient_name,
            "age":          r.age,
            "gender":       r.gender,
            "diagnosis":    r.diagnosis,
            "visit_type":   r.visit_type,
            "visit_time":   r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]


def generate_moh_705(
    db: Session,
    target_date: Optional[date] = None,
) -> Dict[str, Any]:
    """
    MoH 705 summary — Under 5 and Over 5 visit counts grouped by diagnosis.

    Fix [22]: Uses CASE expression to group into two age bands in SQL,
              so the aggregation is correct regardless of how many distinct
              ages are present in the data.
    """
    from sqlalchemy import case

    target_date = target_date or date.today()

    age_band = case(
        (Patient.age < 5, "under_5"),
        else_="over_5",
    ).label("age_band")

    rows = (
        db.query(
            age_band,
            Consultation.diagnosis,
            func.count(Encounter.id).label("count"),
        )
        .join(Encounter, Encounter.patient_id == Patient.id)
        .join(Consultation, Consultation.encounter_id == Encounter.id)
        .filter(func.date(Encounter.created_at) == target_date)
        .group_by("age_band", Consultation.diagnosis)
        .all()
    )

    under_5: Dict[str, int] = {}
    over_5:  Dict[str, int] = {}

    for row in rows:
        diagnosis = row.diagnosis or "Unspecified"
        if row.age_band == "under_5":
            under_5[diagnosis] = under_5.get(diagnosis, 0) + row.count
        else:
            over_5[diagnosis] = over_5.get(diagnosis, 0) + row.count

    return {
        "date":          str(target_date),
        "under_5":       under_5,
        "over_5":        over_5,
        "under_5_total": sum(under_5.values()),
        "over_5_total":  sum(over_5.values()),
    }


def generate_anc_report(
    db: Session,
    month: int,
    year: int,
) -> List[Dict[str, Any]]:
    """
    ANC report for a given month/year.

    Fix [21]: aliased() is used for the ANC model so the row attribute is
              deterministic in both SQLAlchemy 1.x and 2.x.
    """
    from sqlalchemy.orm import aliased

    anc_alias = aliased(ANC, name="anc_alias")

    rows = (
        db.query(
            anc_alias,
            Patient.name.label("patient_name"),
            Patient.age,
        )
        .join(Encounter, Encounter.id == anc_alias.encounter_id)
        .join(Patient, Patient.id == Encounter.patient_id)
        .filter(
            func.extract("month", Encounter.created_at) == month,
            func.extract("year",  Encounter.created_at) == year,
        )
        .order_by(anc_alias.anc_number)
        .all()
    )

    return [
        {
            "anc_number":   r.anc_alias.anc_number,
            "patient_name": r.patient_name,
            "age":          r.age,
            "gravida":      r.anc_alias.gravida,
            "parity":       r.anc_alias.parity,
            "lmp":          str(r.anc_alias.lmp) if r.anc_alias.lmp else None,
            "edd":          str(r.anc_alias.edd) if r.anc_alias.edd else None,
        }
        for r in rows
    ]