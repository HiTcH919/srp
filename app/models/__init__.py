# This file makes the 'models' directory a Python package.

# Import models to make them known to Flask-SQLAlchemy and Flask-Migrate,
# especially if not explicitly imported elsewhere during app initialization.
from .user import User
from .service_order import ServiceOrder
from .officer import Officer
from .security_force_group import SecurityForceGroup
from .female_staff import FemaleStaffMember
from .vehicle import Vehicle
from .service_clause import ServiceOrderClause
from .jurisdiction import JurisdictionInfo
from .deportee_accused import DeporteeAccused
from .document import Document

# Optional: Define __all__ to control 'from app.models import *' behavior
__all__ = [
    'User',
    'ServiceOrder',
    'Officer',
    'SecurityForceGroup',
    'FemaleStaffMember',
    'Vehicle',
    'ServiceOrderClause',
    'JurisdictionInfo',
    'DeporteeAccused',
    'Document'
]
