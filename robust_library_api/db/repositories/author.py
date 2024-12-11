from robust_library_api.db.dao import ExtendedCRUDRepository, repository_for

from robust_library_api.db.models.author import AuthorModel


@repository_for(AuthorModel)
class AuthorRepository(ExtendedCRUDRepository[AuthorModel]):
    async def is_author_exists(self, author_id: int) -> bool:
        return await self.exists(id=author_id)

    async def create_author(self, **author_fields) -> AuthorModel:
        return await self.create(**author_fields)

    async def all_authors(self) -> list[AuthorModel]:
        return await self.find_all()

    async def get_author_by_id(self, author_id: int) -> AuthorModel | None:
        return await self.find_by_id(item_id=author_id)

    async def update_author_by_id(
        self, author_to_update_id: int, **new_fields
    ) -> int:
        return await self.update(fields=new_fields, id=author_to_update_id)

    async def delete_author_by_id(self, author_id: int) -> int:
        return await self.delete(id=author_id)
