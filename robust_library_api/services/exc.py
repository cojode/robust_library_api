class BaseError(Exception):
    def __init__(self, message: str, **details):
        self.message = message
        self.details = details or {}
        super().__init__(message)

class ServiceError(BaseError):
    """Service layer specific exceptions."""
    
class ServiceRepositoryError(BaseError):
    """Service layer exceptions caused by repository errors."""