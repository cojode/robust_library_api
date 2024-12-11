class RepositoryError(Exception):
    """Generic error for repository operations."""


class EntityNotFoundError(RepositoryError):
    """Raised when an entity is not found in the database."""


class UniqueConstraintViolationError(RepositoryError):
    """Raised when a unique constraint is violated."""
