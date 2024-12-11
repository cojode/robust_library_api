from robust_library_api.db.dao import ExtendedCRUDRepository, repository_for

from robust_library_api.db.models.book import BookModel


@repository_for(BookModel)
class BookRepository(ExtendedCRUDRepository[BookModel]):
    async def is_book_exists(self, book_id: int) -> bool:
        return await self.exists(id=book_id)

    async def create_book(self, **book_fields) -> BookModel:
        return await self.create(**book_fields)

    async def all_books(self) -> list[BookModel]:
        return await self.find_all()

    async def get_book_by_id(self, book_id: int) -> BookModel | None:
        return await self.find_by_id(item_id=book_id)

    async def update_book_by_id(
        self, book_to_update_id: int, **new_fields
    ) -> int:
        return await self.update(fields=new_fields, id=book_to_update_id)

    async def delete_book_by_id(self, book_id: int):
        return await self.delete(id=book_id)
