"""
Import all models here so Base.metadata.create_all() can discover every table
regardless of which file is the entry point.
"""

from app.models.user import User            # noqa: F401
from app.models.patient import Patient      # noqa: F401
from app.models.doctor import Doctor        # noqa: F401
from app.models.staff import Staff          # noqa: F401
from app.models.ward import Ward            # noqa: F401
from app.models.encounter import Encounter  # noqa: F401
from app.models.vitals import Vitals        # noqa: F401
from app.models.consultation import Consultation  # noqa: F401
from app.models.lab import LabRequest       # noqa: F401
from app.models.pharmacy import Prescription  # noqa: F401
from app.models.inventory import Inventory  # noqa: F401
from app.models.billing import Billing      # noqa: F401
from app.models.anc import ANC             # noqa: F401
from app.models.procedure import Procedure  # noqa: F401