from robust_library_api.db.repositories.book import BookRepository
from robust_library_api.db.repositories.author import AuthorRepository

from robust_library_api.web.api.books.schema import (
    BookResponse,
    BookListResponse,
    BookCountResponse
)

class BookService:
    def __init__(self, book_repository: BookRepository, author_repository: AuthorRepository):
        self.book_repository: BookRepository = book_repository
        self.author_repository: AuthorRepository = author_repository

    async def book_creation(self, **book_creation_fields):
        author_id = book_creation_fields.get('author_id', None)
        if not await self.author_repository.is_author_exists(
            author_id=author_id
        ):
            return BookResponse(
                status="error",
                message=f"Author with following ID does not exists: {author_id}.",
                data=None
            )
        created_book = await self.book_repository.create_book(**book_creation_fields)
        return BookResponse(
            status="success",
            message="Book created sucessfully.",
            data=dict(created_book),
        )

    async def all_books_list(self):
        all_books = await self.book_repository.all_books()
        return BookListResponse(
            status="success",
            message="Books fetched successfully.",
            data=[dict(book) for book in all_books],
        )
        
    async def obtain_book_information(self, book_id: int):
        book_entity = await self.book_repository.get_book_by_id(book_id=book_id)
        if not book_entity:
            return BookResponse(
                status="error",
                message=f"Book with ID {book_id} not found.",
                data=None,
            )
        return BookResponse(
            status="success",
            message="Book information fetched successfully.",
            data=dict(book_entity),
        )
    

    async def update_book_information(
        self, book_id: int, **new_book_fields
    ):
        if not await self.book_repository.is_book_exists(id=book_id):
            return BookCountResponse(
                status="error",
                message=f"Book with ID {book_id} not found.",
                data=0
            )
        
        new_book_fields_without_ellipsis = {
            field: value
            for field, value in new_book_fields.dict().items()
            if value is not Ellipsis
        }
        
        author_id = new_book_fields.get('author_id', None)
        
        if author_id is not None and not await self.author_repository.is_author_exists(author_id=author_id):
            return BookCountResponse(
                status="error",
                message=f"Author with ID {author_id} not found.",
                data=0
            )
        
        update_count = await self.book_repository.update_book_by_id(
            book_to_update_id=book_id, **new_book_fields_without_ellipsis
        )
        return BookCountResponse(
            status="success",
            message=f"{update_count} book(s) updated." if update_count > 0 else "No book updated.",
            data=update_count,
        )

    async def delete_book(self, book_id: int):
        delete_count = await self.book_repository.delete_book_by_id(book_id=book_id)
        return BookCountResponse(
            status="success" if delete_count > 0 else "error",
            message=f"{delete_count} book(s) deleted." 
            if delete_count > 0 
            else "No book deleted. Book with ID {book_id} not found.",
            data=delete_count,
        )
