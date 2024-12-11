from robust_library_api.db.repositories.book import BookRepository
from robust_library_api.db.repositories.author import AuthorRepository

from robust_library_api.db.dao.exc import ForeignKeyViolation

from robust_library_api.services.utils import (
    repository_fallback, 
    model_row_to_dict
)

from robust_library_api.db.models.author import AuthorModel
from robust_library_api.db.models.book import BookModel

from robust_library_api.services.book.exc import (
    BookNotFoundBookError,
    BookNotFoundAuthorError,
    BookNotFoundDeletedError,
    BookServiceRepositoryError,
    BookStillObtainsBorrowsError
)

from robust_library_api.web.api.books.schema import (
    ResponseBook,
    ResponseBookCount,
    ResponseBookList
)

class BookService:
    def __init__(self, book_repository: BookRepository, author_repository: AuthorRepository):
        self.book_repository: BookRepository = book_repository
        self.author_repository: AuthorRepository = author_repository
        
    @repository_fallback(BookServiceRepositoryError)
    async def _verify_extract_author(self, author_id: int) -> AuthorModel:
        author_entity = await self.author_repository.get_author_by_id(author_id=author_id)
        if not author_entity:
            raise BookNotFoundAuthorError(author_id)
        return author_entity

    @repository_fallback(BookServiceRepositoryError)
    async def _verify_extract_book(self, book_id: int) -> BookModel:
        book_entity = await self.book_repository.get_book_by_id(book_id=book_id)
        if not book_entity:
            raise BookNotFoundBookError(book_id)
        return book_entity

    @repository_fallback(BookServiceRepositoryError)
    async def book_creation(self, **book_creation_fields):
        author_id = book_creation_fields.get('author_id', None)
        await self._verify_extract_author(author_id=author_id)
        created_book = await self.book_repository.create_book(**book_creation_fields)
        return ResponseBook(
            message="Book created sucessfully.",
            data=model_row_to_dict(created_book),
        )

    @repository_fallback(BookServiceRepositoryError)
    async def all_books_list(self):
        all_books = await self.book_repository.all_books()
        return ResponseBookList(
            status="success",
            message="Books fetched successfully.",
            data=[model_row_to_dict(book) for book in all_books],
        )
    
    @repository_fallback(BookServiceRepositoryError)
    async def obtain_book_information(self, book_id: int):
        book_entity = await self._verify_extract_book(book_id=book_id)
        return ResponseBook(
            message="Book information fetched successfully.",
            data=model_row_to_dict(book_entity),
        )
    
    @repository_fallback(BookServiceRepositoryError)
    async def update_book_information(
        self, book_id: int, **new_book_fields
    ):
        await self._verify_extract_book(book_id=book_id)
        
        author_id = new_book_fields.get('author_id', None)
        
        new_book_fields_without_nones = {
            field: value
            for field, value in new_book_fields.items()
            if value is not None
        }
        
        if author_id is not None:
            await self._verify_extract_author(author_id=author_id)
        
        update_count = await self.book_repository.update_book_by_id(
            book_to_update_id=book_id, **new_book_fields_without_nones
        )
        
        return ResponseBookCount(
            message=f"{update_count} book(s) updated.",
            data=update_count,
        )

    @repository_fallback(BookServiceRepositoryError)
    async def delete_book(self, book_id: int):
        try:
            delete_count = await self.book_repository.delete_book_by_id(book_id=book_id)
        except ForeignKeyViolation:
            raise BookStillObtainsBorrowsError(book_id)
        if delete_count == 0:
            raise BookNotFoundDeletedError(book_id)
        return ResponseBookCount(
            message=f"{delete_count} book(s) deleted.",
            data=delete_count,
        )
