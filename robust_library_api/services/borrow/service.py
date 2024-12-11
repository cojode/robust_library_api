from datetime import date

from robust_library_api.db.repositories.borrow import BorrowRepository
from robust_library_api.db.repositories.book import BookRepository

from robust_library_api.services.utils import (
    repository_fallback, 
    model_row_to_dict
)

from robust_library_api.db.models.book import BookModel
from robust_library_api.db.models.borrow import BorrowModel

from robust_library_api.services.borrow.exc import (
    BorrowNotFoundBorrowError,
    BorrowNotFoundBookError,
    BorrowBookExhaustedError,
    BorrowServiceRepositoryError,
    BorrowAlreadyClosedError
)

from robust_library_api.web.api.borrows.schema import (
    ResponseBorrow,
    ResponseBorrowList
)

class BorrowService:
    def __init__(self, borrow_repository: BorrowRepository, book_repository: BookRepository):
        self.borrow_repository: BorrowRepository = borrow_repository
        self.book_repository: BookRepository = book_repository
        
    @repository_fallback(BorrowServiceRepositoryError)
    async def _verify_extract_book(self, book_id: int) -> BookModel:
        book_entity = await self.book_repository.get_book_by_id(book_id=book_id)
        if not book_entity:
            raise BorrowNotFoundBookError(book_id)
        return book_entity

    @repository_fallback(BorrowServiceRepositoryError)
    async def _verify_extract_borrow(self, borrow_id: int) -> BorrowModel:
        borrow_entity = await self.borrow_repository.get_borrow_by_id(borrow_id=borrow_id)
        if not borrow_entity:
            raise BorrowNotFoundBorrowError(borrow_id)
        return borrow_entity

    @repository_fallback(BorrowServiceRepositoryError)
    async def borrow_creation(self, **borrow_creation_fields):
        book_id = borrow_creation_fields.get('book_id', None)
        
        book_entity = await self._verify_extract_book(book_id=book_id)
        
        if book_entity.remaining_amount == 0:
            raise BorrowBookExhaustedError(book_entity.id)
        
        book_entity.remaining_amount -= 1
        
        await self.book_repository.save(book_entity)
        
        created_borrow = await self.borrow_repository.create_borrow(
            **borrow_creation_fields,
            date_of_issue=date.today()
        )
        
        return ResponseBorrow(
            message="Borrow created sucessfully.",
            data=model_row_to_dict(created_borrow),
        )

    @repository_fallback(BorrowServiceRepositoryError)
    async def all_borrows_list(self):
        all_borrows = await self.borrow_repository.all_borrows()
        return ResponseBorrowList(
            status="success",
            message="Borrows fetched successfully.",
            data=[model_row_to_dict(borrow) for borrow in all_borrows],
        )
    
    @repository_fallback(BorrowServiceRepositoryError)
    async def obtain_borrow_information(self, borrow_id: int):
        borrow_entity = await self._verify_extract_borrow(borrow_id=borrow_id)
        return ResponseBorrow(
            message="Borrow information fetched successfully.",
            data=model_row_to_dict(borrow_entity),
        )
    
    @repository_fallback(BorrowServiceRepositoryError)
    async def close_borrow(self, borrow_id: int):
        borrow_entity = await self._verify_extract_borrow(borrow_id=borrow_id)
        
        if borrow_entity.date_of_return is not None:
            raise BorrowAlreadyClosedError(already_closed_borrow_id=borrow_id)
        
        book_entity = await self.book_repository.find_by_id(borrow_entity.book_id)
        
        book_entity.remaining_amount += 1
        
        await self.book_repository.save(book_entity)
        
        borrow_entity.date_of_return = date.today()
        
        await self.borrow_repository.save(borrow_entity)
        
        return borrow_entity