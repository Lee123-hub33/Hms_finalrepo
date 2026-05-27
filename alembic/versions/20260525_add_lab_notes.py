"""add technician_notes to lab_requests

Revision ID: 20260525_add_lab_notes
Revises: 20260520_add_encounter_fields
Create Date: 2026-05-25 12:16:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20260525_add_lab_notes'
down_revision = '20260520_add_encounter_fields'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('lab_requests', sa.Column('technician_notes', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('lab_requests', 'technician_notes')
