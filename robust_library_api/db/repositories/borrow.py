from robust_library_api.db.dao import ExtendedCRUDRepository, repository_for

from robust_library_api.db.models.borrow import BorrowModel


@repository_for(BorrowModel)
class BorrowRepository(ExtendedCRUDRepository[BorrowModel]):
    async def is_borrow_exists(self, borrow_id: int) -> bool:
        return await self.exists(id=borrow_id)

    async def create_borrow(self, **borrow_fields) -> BorrowModel:
        return await self.create(**borrow_fields)

    async def all_borrows(self) -> list[BorrowModel]:
        return await self.find_all()

    async def get_borrow_by_id(self, borrow_id: int) -> BorrowModel | None:
        return await self.find_by_id(item_id=borrow_id)

    async def update_borrow_by_id(self, borrow_id: int, **new_fields):
        return await self.update(fields=new_fields, id=borrow_id)