"""Routes for swagger and redoc."""

from .crud import CRUDRepository
from .extended import ExtendedCRUDRepository
from .exc import RepositoryError

from .interface import repository_for, extended_crud_repository_for, crud_repository_for

__all__ = ["repository_for", "extended_crud_repository_for", "crud_repository_for"]
