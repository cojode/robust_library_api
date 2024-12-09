"""Routes for swagger and redoc."""

from nir_myrmiaka.db.repositories.crud.crud import CRUDRepository
from nir_myrmiaka.db.repositories.crud.extended import ExtendedCRUDRepository

__all__ = ["ExtendedCRUDRepository", "CRUDRepository"]
