from sqlalchemy.orm import DeclarativeBase

from robust_library_api.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
