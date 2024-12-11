from robust_library_api.services.exc import (
    ServiceError,
    ServiceRepositoryError
)

class AuthorServiceError(ServiceError): ...
    
class AuthorNotFoundError(AuthorServiceError):
    def __init__(self, not_found_author_id: int, **details):
        super().__init__(f"Author with ID {not_found_author_id} not found.")
        
class AuthorNotFoundDeletedError(AuthorServiceError):
    def __init__(self, not_deleted_author_id: int, **details):
        super().__init__(f"0 author(s) deleted. Author with ID {not_deleted_author_id} not found.")

class AuthorServiceRepositoryError(ServiceRepositoryError):
    def __init__(self, error_message_details: str = None):
        super().__init__(f"Author service failed with repository error. {error_message_details if error_message_details else 'No details provided.'}")