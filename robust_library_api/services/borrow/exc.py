from robust_library_api.services.exc import (
    ServiceError,
    ServiceRepositoryError
)

class BorrowServiceError(ServiceError): ...
    
class BorrowNotFoundBorrowError(BorrowServiceError):
    def __init__(self, not_found_book_id: int, **details):
        super().__init__(f"Borrow with ID {not_found_book_id} not found.")

class BorrowNotFoundBookError(BorrowServiceError):
    def __init__(self, not_found_author_id: int, **details):
        super().__init__(f"Book with ID {not_found_author_id} not found.")

class BorrowBookExhaustedError(BorrowServiceError):
    def __init__(self, exhausted_book_id: int, **details):
        super().__init__(f"Can't borrow: book with ID {exhausted_book_id} are over - no book left.")

class BorrowAlreadyClosedError(BorrowServiceError):
    def __init__(self, already_closed_borrow_id: int, **details):
        super().__init__(f"Can't close borrow: borrow with ID {already_closed_borrow_id} already closed.")

class BorrowServiceRepositoryError(ServiceRepositoryError):
    def __init__(self, error_message_details: str = None):
        super().__init__(f"Borrow service failed with repository error. {error_message_details if error_message_details else 'No details provided.'}")