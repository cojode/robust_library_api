from robust_library_api.services.exc import (
    ServiceError,
    ServiceRepositoryError
)

class BookServiceError(ServiceError): ...
    
class BookNotFoundBookError(BookServiceError):
    def __init__(self, not_found_book_id: int, **details):
        super().__init__(f"Book with ID {not_found_book_id} not found.")

class BookNotFoundAuthorError(BookServiceError):
    def __init__(self, not_found_author_id: int, **details):
        super().__init__(f"Author with ID {not_found_author_id} not found.")
        
class BookNotFoundDeletedError(BookServiceError):
    def __init__(self, not_deleted_book_id: int, **details):
        super().__init__(f"0 book(s) deleted. Book with ID {not_deleted_book_id} not found.")

class BookServiceRepositoryError(ServiceRepositoryError):
    def __init__(self, error_message_details: str = None):
        super().__init__(f"Book service failed with repository error. {error_message_details if error_message_details else 'No details provided.'}")
        
class BookStillObtainsBorrowsError(BookServiceError):
    def __init__(self, book_id: int, **details):
        super().__init__(f"Can't delete book: Book with ID {book_id} still has related borrows in table (borrow).")