# Import tables need for alembic migration work.

from src.models.customer import CustomerTable, CustomerAddressTable  # noqa: F401
from src.database.db import Base  # noqa: F401
