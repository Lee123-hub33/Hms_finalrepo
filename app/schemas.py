"""
Pydantic v2 request/response schemas for all resources.

Fix [15]: All endpoints now use typed schema bodies instead of raw query params.
Fix [16]: Response schemas give every endpoint a documented, validated output shape.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from app.models.staff import RoleEnum
from app.models.encounter import VisitTypeEnum, PatientStatusEnum, TriageLevelEnum
from app.models.lab import LabStatusEnum
from app.models.pharmacy import PharmacyStatusEnum
from app.models.billing import BillingStatusEnum
from app.models.inventory import ItemCategoryEnum


# ── Auth ──────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)


class UserOut(BaseModel):
    id: int
    username: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    is_active: Optional[bool] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None


class RefreshRequest(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    username: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


# ── Patient ───────────────────────────────────────────────────────────────────

class PatientCreate(BaseModel):
    name:   str = Field(..., min_length=1, max_length=255)
    age:    int = Field(..., ge=0, le=150)
    gender: str = Field(..., min_length=1, max_length=10)

    @field_validator("gender")
    @classmethod
    def capitalise_gender(cls, v: str) -> str:
        return v.strip().capitalize()


class PatientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    age: Optional[int] = Field(None, ge=0, le=150)
    gender: Optional[str] = Field(None, min_length=1, max_length=10)

    @field_validator("gender")
    @classmethod
    def capitalise_gender(cls, v: Optional[str]) -> Optional[str]:
        return v.strip().capitalize() if v else v


class PatientOut(PatientCreate):
    id:         int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Doctor ────────────────────────────────────────────────────────────────────

class DoctorCreate(BaseModel):
    name:           str = Field(..., min_length=1, max_length=255)
    specialization: str = Field(..., max_length=255)
    license_number: str = Field(..., max_length=100)
   

class DoctorOut(DoctorCreate):
    id: int

    model_config = {"from_attributes": True}


# ── Staff ─────────────────────────────────────────────────────────────────────

class StaffCreate(BaseModel):
    name:       str      = Field(..., min_length=1, max_length=255)
    role:       RoleEnum
    department: Optional[str] = None
    user_id:    int


class StaffOut(StaffCreate):
    id: int

    model_config = {"from_attributes": True}


# ── Procedure ─────────────────────────────────────────────────────────────────

class ProcedureCreate(BaseModel):
    encounter_id:   int
    procedure_name: str = Field(..., min_length=1, max_length=255)
    description:    Optional[str] = None
    cost:           float = Field(0.0, ge=0)

class ProcedureOut(ProcedureCreate):
    id:           int
    performed_at: datetime

    model_config = {"from_attributes": True}


# ── Ward ──────────────────────────────────────────────────────────────────────

class WardCreate(BaseModel):
    ward_name: str = Field(..., min_length=1, max_length=255)
    capacity:  int = Field(..., gt=0)


class WardOut(BaseModel):
    id:                int
    ward_name:         str
    capacity:          int
    current_occupancy: int

    model_config = {"from_attributes": True}


# ── Encounter ─────────────────────────────────────────────────────────────────

class EncounterBase(BaseModel):
    patient_id:     int
    visit_type:     VisitTypeEnum
    patient_status: PatientStatusEnum = PatientStatusEnum.pending
    ward_id:        Optional[int] = Field(None, gt=0)
    triage_level:   Optional[TriageLevelEnum] = TriageLevelEnum.normal


class EncounterCreate(EncounterBase):
    @model_validator(mode="after")
    def validate_ward_assignment(cls, values):
        if values.patient_status != PatientStatusEnum.inpatient and values.ward_id is not None:
            raise ValueError("ward_id may only be provided for inpatient status.")
        if values.patient_status == PatientStatusEnum.inpatient and values.ward_id is None:
            raise ValueError("ward_id is required when status is Inpatient.")
        return values


class EncounterOut(EncounterBase):
    id:         int
    staff_id:   int
    created_at: datetime
    triage_level: TriageLevelEnum
    bed_number: Optional[str]
    discharged: bool
    discharge_notes: Optional[str]
    discharged_at: Optional[datetime]

    model_config = {"from_attributes": True}


# ── Vitals ────────────────────────────────────────────────────────────────────

class VitalsUpdate(BaseModel):
    encounter_id:   int
    temperature:    Optional[float] = Field(None, ge=30.0, le=45.0, description="°C")
    blood_pressure: Optional[str]   = Field(None, max_length=20, examples=["120/80"])
    weight:         Optional[float] = Field(None, gt=0, description="kg")
    height:         Optional[float] = Field(None, gt=0, description="cm")
    muac:           Optional[float] = Field(None, gt=0, description="cm")


class VitalsOut(VitalsUpdate):
    id:          int
    recorded_at: datetime

    model_config = {"from_attributes": True}


# ── Consultation ──────────────────────────────────────────────────────────────

class ConsultationCreate(BaseModel):
    encounter_id:    int
    chief_complaint: Optional[str] = None
    clinical_notes:  Optional[str] = None
    diagnosis:       str = Field(..., min_length=1, max_length=500)


class ConsultationOut(ConsultationCreate):
    id:         int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Lab ───────────────────────────────────────────────────────────────────────

class LabRequestCreate(BaseModel):
    encounter_id:   int
    test_requested: str = Field(..., min_length=1, max_length=255)


class LabResultUpdate(BaseModel):
    results: str = Field(..., min_length=1)
    technician_notes: Optional[str] = None


class LabOut(BaseModel):
    id:             int
    encounter_id:   int
    test_requested: str
    results:        Optional[str]
    technician_notes: Optional[str]
    status:         LabStatusEnum
    requested_at:   datetime
    completed_at:   Optional[datetime]
    patient_name:   Optional[str] = None

    model_config = {"from_attributes": True}


# ── Pharmacy ──────────────────────────────────────────────────────────────────

class PrescriptionCreate(BaseModel):
    encounter_id:         int
    prescription_details: str = Field(..., min_length=1)


class PrescriptionOut(PrescriptionCreate):
    id:           int
    status:       PharmacyStatusEnum
    created_at:   datetime
    dispensed_at: Optional[datetime]

    model_config = {"from_attributes": True}


# ── Billing ───────────────────────────────────────────────────────────────────

class BillingCreate(BaseModel):
    encounter_id: int
    service_type: str   = Field(..., min_length=1, max_length=255)
    amount:       float = Field(..., gt=0)


class BillingOut(BillingCreate):
    id:         int
    status:     BillingStatusEnum
    created_at: datetime
    paid_at:    Optional[datetime]

    model_config = {"from_attributes": True}


# ── ANC ───────────────────────────────────────────────────────────────────────

class ANCCreate(BaseModel):
    encounter_id: int
    anc_number:   str = Field(..., min_length=1, max_length=50)
    gravida:      int = Field(..., ge=1)
    parity:       int = Field(..., ge=0)
    lmp:          Optional[date] = None
    edd:          Optional[date] = None


class ANCOut(ANCCreate):
    id: int

    model_config = {"from_attributes": True}


# ── Inventory ─────────────────────────────────────────────────────────────────

class InventoryCreate(BaseModel):
    item_name:     str             = Field(..., min_length=1, max_length=255)
    category:      ItemCategoryEnum
    quantity:      int             = Field(..., ge=0)
    reorder_level: int             = Field(10, ge=0)


class InventoryOut(InventoryCreate):
    id:           int
    needs_reorder: bool

    model_config = {"from_attributes": True}


class InventoryAdjust(BaseModel):
    delta: int


# ── Reports ───────────────────────────────────────────────────────────────────

class DailyRegistryRow(BaseModel):
    encounter_id: int
    patient_name: str
    age:          int
    gender:       str
    diagnosis:    Optional[str]
    visit_type:   str
    visit_time:   Optional[str]


class MOH705Report(BaseModel):
    date:          str
    under_5:       dict
    over_5:        dict
    under_5_total: int
    over_5_total:  int


class ANCReportRow(BaseModel):
    anc_number:   str
    patient_name: str
    age:          int
    gravida:      int
    parity:       int
    lmp:          Optional[str]
    edd:          Optional[str]