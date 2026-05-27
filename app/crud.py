"""
Database operations — all queries go through SQLAlchemy ORM.

SQL injection note: ORM uses parameterised queries for every operation.
No raw SQL strings (text()) are used anywhere in this file.
"""

from datetime import datetime, timezone
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.anc import ANC
from app.models.billing import Billing, BillingStatusEnum
from app.models.consultation import Consultation
from app.models.doctor import Doctor
from app.models.encounter import Encounter
from app.models.inventory import Inventory
from app.models.lab import LabRequest, LabStatusEnum
from app.models.patient import Patient
from app.models.pharmacy import Prescription, PharmacyStatusEnum
from app.models.procedure import Procedure
from app.models.staff import Staff
from app.models.vitals import Vitals
from app.models.ward import Ward
from app.models.refresh_token import RefreshToken
from app.models.user import User
from app.schemas import (
    ANCCreate, BillingCreate, ConsultationCreate, DoctorCreate,
    EncounterCreate, InventoryCreate, LabRequestCreate, PatientCreate,
    PrescriptionCreate, ProcedureCreate, StaffCreate, VitalsUpdate, WardCreate,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_or_404(db: Session, model, record_id: int):
    """Generic fetch-or-raise helper — keeps all route handlers DRY."""
    obj = db.get(model, record_id)
    if obj is None:
        raise HTTPException(
            status_code=404,
            detail=f"{model.__tablename__.rstrip('s').capitalize()} {record_id} not found.",
        )
    return obj


def get_encounter_or_404(db: Session, encounter_id: int) -> Encounter:
    return _get_or_404(db, Encounter, encounter_id)


# ── Patients ──────────────────────────────────────────────────────────────────

def create_patient(db: Session, data: PatientCreate) -> Patient:
    patient = Patient(**data.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def get_patients(db: Session, skip: int = 0, limit: int = 100) -> List[Patient]:
    return db.query(Patient).offset(skip).limit(limit).all()


def get_patient_by_id(db: Session, patient_id: int) -> Patient:
    """Raises 404 if patient does not exist."""
    return _get_or_404(db, Patient, patient_id)


# ── Doctors ───────────────────────────────────────────────────────────────────

def create_doctor(db: Session, data: DoctorCreate) -> Doctor:
    doctor = Doctor(**data.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def get_doctors(db: Session, skip: int = 0, limit: int = 100) -> List[Doctor]:
    return db.query(Doctor).offset(skip).limit(limit).all()


def get_doctor_by_id(db: Session, doctor_id: int) -> Doctor:
    return _get_or_404(db, Doctor, doctor_id)


# ── Staff ─────────────────────────────────────────────────────────────────────

def create_staff(db: Session, data: StaffCreate) -> Staff:
    staff = Staff(**data.model_dump())
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff


def get_staff(db: Session, skip: int = 0, limit: int = 100) -> List[Staff]:
    return db.query(Staff).offset(skip).limit(limit).all()


def get_staff_by_id(db: Session, staff_id: int) -> Staff:
    return _get_or_404(db, Staff, staff_id)


# ── Wards ─────────────────────────────────────────────────────────────────────

def create_ward(db: Session, data: WardCreate) -> Ward:
    ward = Ward(**data.model_dump())
    db.add(ward)
    db.commit()
    db.refresh(ward)
    return ward


def get_wards(db: Session, skip: int = 0, limit: int = 100) -> List[Ward]:
    return db.query(Ward).offset(skip).limit(limit).all()


# ── Encounters ────────────────────────────────────────────────────────────────

def create_encounter(db: Session, data: EncounterCreate, staff_id: int) -> Encounter:
    if data.ward_id is not None:
        ward = _get_or_404(db, Ward, data.ward_id)
        if ward.current_occupancy >= ward.capacity:
            raise HTTPException(status_code=409, detail="Ward is full.")
        ward.current_occupancy += 1
        db.add(ward)

    encounter = Encounter(**data.model_dump(), staff_id=staff_id)
    db.add(encounter)
    db.commit()
    db.refresh(encounter)
    return encounter


def get_encounters_by_patient(db: Session, patient_id: int, skip: int = 0, limit: int = 100) -> List[Encounter]:
    """Return all encounters for a given patient (visit history)."""
    # Ensure patient exists — mirrors get_patient_by_id semantics
    _get_or_404(db, Patient, patient_id)
    return (
        db.query(Encounter)
        .filter(Encounter.patient_id == patient_id)
        .order_by(Encounter.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


# ── Vitals ────────────────────────────────────────────────────────────────────

def upsert_vitals(db: Session, data: VitalsUpdate) -> Vitals:
    get_encounter_or_404(db, data.encounter_id)
    vitals = (
        db.query(Vitals)
        .filter(Vitals.encounter_id == data.encounter_id)
        .first()
    )
    if vitals:
        for field, value in data.model_dump(
            exclude={"encounter_id"}, exclude_none=True
        ).items():
            setattr(vitals, field, value)
    else:
        vitals = Vitals(**data.model_dump())
        db.add(vitals)
    db.commit()
    db.refresh(vitals)
    return vitals


# ── Consultation ──────────────────────────────────────────────────────────────

def create_consultation(db: Session, data: ConsultationCreate) -> Consultation:
    get_encounter_or_404(db, data.encounter_id)
    consult = Consultation(**data.model_dump())
    db.add(consult)
    db.commit()
    db.refresh(consult)
    return consult


# ── Procedure ─────────────────────────────────────────────────────────────────

def create_procedure(db: Session, data: ProcedureCreate) -> Procedure:
    get_encounter_or_404(db, data.encounter_id)
    procedure = Procedure(**data.model_dump())
    db.add(procedure)
    db.commit()
    db.refresh(procedure)
    return procedure


# ── Lab ───────────────────────────────────────────────────────────────────────

def create_lab_request(db: Session, data: LabRequestCreate) -> LabRequest:
    get_encounter_or_404(db, data.encounter_id)
    lab = LabRequest(**data.model_dump())
    db.add(lab)
    db.commit()
    db.refresh(lab)
    return lab


def complete_lab_request(db: Session, lab_id: int, results: str, notes: Optional[str] = None) -> LabRequest:
    lab = _get_or_404(db, LabRequest, lab_id)
    lab.results      = results
    lab.technician_notes = notes
    lab.status       = LabStatusEnum.completed
    lab.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(lab)
    return lab


# ── Pharmacy ──────────────────────────────────────────────────────────────────

def create_prescription(db: Session, data: PrescriptionCreate) -> Prescription:
    get_encounter_or_404(db, data.encounter_id)
    rx = Prescription(**data.model_dump())
    db.add(rx)
    db.commit()
    db.refresh(rx)
    return rx


def dispense_prescription(db: Session, prescription_id: int) -> Prescription:
    rx              = _get_or_404(db, Prescription, prescription_id)
    rx.status       = PharmacyStatusEnum.dispensed
    rx.dispensed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(rx)
    return rx


# ── Billing ───────────────────────────────────────────────────────────────────

def create_bill(db: Session, data: BillingCreate) -> Billing:
    get_encounter_or_404(db, data.encounter_id)
    bill = Billing(**data.model_dump())
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill


def mark_bill_paid(db: Session, bill_id: int) -> Billing:
    bill         = _get_or_404(db, Billing, bill_id)
    bill.status  = BillingStatusEnum.paid
    bill.paid_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(bill)
    return bill


# ── ANC ───────────────────────────────────────────────────────────────────────

def create_anc(db: Session, data: ANCCreate) -> ANC:
    get_encounter_or_404(db, data.encounter_id)
    anc = ANC(**data.model_dump())
    db.add(anc)
    db.commit()
    db.refresh(anc)
    return anc


# ── Inventory ─────────────────────────────────────────────────────────────────

def create_inventory_item(db: Session, data: InventoryCreate) -> Inventory:
    item = Inventory(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_low_stock(db: Session) -> List[Inventory]:
    return (
        db.query(Inventory)
        .filter(Inventory.quantity <= Inventory.reorder_level)
        .all()
    )


def get_inventory(db: Session, skip: int = 0, limit: int = 100) -> List[Inventory]:
    return db.query(Inventory).offset(skip).limit(limit).all()


def adjust_inventory(db: Session, item_id: int, delta: int) -> Inventory:
    item = _get_or_404(db, Inventory, item_id)
    item.quantity = max(0, item.quantity + delta)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def get_lab_requests_by_encounter(db: Session, encounter_id: int) -> List[LabRequest]:
    encounter = get_encounter_or_404(db, encounter_id)
    patient = db.query(Patient).filter(Patient.id == encounter.patient_id).first()
    patient_name = patient.name if patient else None

    requests = db.query(LabRequest).filter(LabRequest.encounter_id == encounter_id).all()
    for lab in requests:
        lab.patient_name = patient_name
    return requests


def get_all_lab_requests(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[LabStatusEnum] = None,
) -> List[LabRequest]:
    query = db.query(LabRequest, Patient.name.label("patient_name")).join(
        Encounter, LabRequest.encounter_id == Encounter.id
    ).join(
        Patient, Encounter.patient_id == Patient.id
    )
    if status is not None:
        query = query.filter(LabRequest.status == status)
    results = query.order_by(LabRequest.requested_at.desc()).offset(skip).limit(limit).all()

    output = []
    for lab, patient_name in results:
        lab.patient_name = patient_name
        output.append(lab)
    return output


def get_billing_by_encounter(db: Session, encounter_id: int) -> List[Billing]:
    get_encounter_or_404(db, encounter_id)
    return db.query(Billing).filter(Billing.encounter_id == encounter_id).all()


def get_vitals_by_encounter(db: Session, encounter_id: int) -> Vitals:
    get_encounter_or_404(db, encounter_id)
    v = db.query(Vitals).filter(Vitals.encounter_id == encounter_id).first()
    if not v:
        raise HTTPException(status_code=404, detail=f"Vitals for encounter {encounter_id} not found.")
    return v


def update_patient(db: Session, patient_id: int, data: dict) -> Patient:
    patient = _get_or_404(db, Patient, patient_id)
    for k, v in data.items():
        setattr(patient, k, v)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def discharge_encounter(db: Session, encounter_id: int, notes: Optional[str] = None) -> Encounter:
    enc = _get_or_404(db, Encounter, encounter_id)
    if enc.ward_id is not None and not enc.discharged:
        ward = _get_or_404(db, Ward, enc.ward_id)
        ward.current_occupancy = max(0, ward.current_occupancy - 1)
        db.add(ward)

    enc.discharged = True
    enc.discharge_notes = notes
    enc.discharged_at = datetime.now(timezone.utc)
    db.add(enc)
    db.commit()
    db.refresh(enc)
    return enc


def assign_bed(db: Session, encounter_id: int, bed_number: str) -> Encounter:
    enc = _get_or_404(db, Encounter, encounter_id)
    enc.bed_number = bed_number
    db.add(enc)
    db.commit()
    db.refresh(enc)
    return enc


# ── Refresh / Password Reset Tokens ──────────────────────────────────────────
import hashlib
import secrets
from datetime import timedelta


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_refresh_token(db: Session, user_id: int, expires_minutes: int = 60 * 24 * 30) -> str:
    raw = secrets.token_urlsafe(32)
    token_hash = _hash_token(raw)
    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=expires_minutes)
    rt = RefreshToken(user_id=user_id, token_hash=token_hash, created_at=now, expires_at=expires, revoked=False, token_type="refresh")
    db.add(rt)
    db.commit()
    return raw


def get_user_by_refresh_token(db: Session, token: str) -> Optional[User]:
    token_hash = _hash_token(token)
    now = datetime.now(timezone.utc)
    rt = (
        db.query(RefreshToken)
        .filter(RefreshToken.token_hash == token_hash)
        .filter(RefreshToken.revoked == False)
        .filter(RefreshToken.expires_at > now)
        .first()
    )
    if not rt:
        return None
    return db.get(User, rt.user_id)


def revoke_refresh_token(db: Session, token: str) -> None:
    token_hash = _hash_token(token)
    rt = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    if rt:
        rt.revoked = True
        db.commit()


def create_password_reset_token(db: Session, user_id: int, expires_minutes: int = 60) -> str:
    raw = secrets.token_urlsafe(24)
    token_hash = _hash_token(raw)
    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=expires_minutes)
    rt = RefreshToken(user_id=user_id, token_hash=token_hash, created_at=now, expires_at=expires, revoked=False, token_type="password_reset")
    db.add(rt)
    db.commit()
    return raw


def verify_password_reset_token(db: Session, token: str) -> Optional[User]:
    token_hash = _hash_token(token)
    now = datetime.now(timezone.utc)
    rt = (
        db.query(RefreshToken)
        .filter(RefreshToken.token_hash == token_hash)
        .filter(RefreshToken.revoked == False)
        .filter(RefreshToken.expires_at > now)
        .filter(RefreshToken.token_type == "password_reset")
        .first()
    )
    if not rt:
        return None
    # consume token
    rt.revoked = True
    db.commit()
    return db.get(User, rt.user_id)