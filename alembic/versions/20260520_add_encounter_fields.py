"""Add triage and discharge fields to encounters and add Pending patient status

Revision ID: 20260520_add_encounter_fields
Revises: 
Create Date: 2026-05-20 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260520_add_encounter_fields'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    # 1) add enum value 'pending' to patientstatusenum if not present
    try:
        conn.exec_driver_sql("""
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_type t
                JOIN pg_enum e ON t.oid = e.enumtypid
                WHERE t.typname = 'patientstatusenum' AND e.enumlabel = 'pending'
            ) THEN
                ALTER TYPE patientstatusenum ADD VALUE 'pending';
            END IF;
        END$$;
        """)
    except Exception:
        # best-effort: if type or value already exists or DB doesn't support, ignore
        pass

    # 2) add missing columns to encounters (safe: check existence first)
    cols = [
        ("triage_level", "VARCHAR(32)", "DEFAULT 'normal' NOT NULL"),
        ("bed_number", "VARCHAR(32)", "NULL"),
        ("discharged", "BOOLEAN", "DEFAULT FALSE NOT NULL"),
        ("discharge_notes", "VARCHAR(1000)", "NULL"),
        ("discharged_at", "TIMESTAMP WITH TIME ZONE", "NULL"),
    ]

    for name, type_, attrs in cols:
        exists = conn.exec_driver_sql(
            "SELECT 1 FROM information_schema.columns WHERE table_name='encounters' AND column_name='%s'" % name
        ).first()
        if not exists:
            conn.exec_driver_sql(f"ALTER TABLE encounters ADD COLUMN {name} {type_} {attrs};")


def downgrade() -> None:
    conn = op.get_bind()

    # Drop columns if present
    for name in ("discharged_at", "discharge_notes", "discharged", "bed_number", "triage_level"):
        exists = conn.exec_driver_sql(
            "SELECT 1 FROM information_schema.columns WHERE table_name='encounters' AND column_name='%s'" % name
        ).first()
        if exists:
            conn.exec_driver_sql(f"ALTER TABLE encounters DROP COLUMN IF EXISTS {name};")

    # Note: removing an enum value is not supported safely across PG versions; skip
