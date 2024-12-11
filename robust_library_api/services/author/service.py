from robust_library_api.db.repositories.author import AuthorRepository
from robust_library_api.db.models.author import AuthorModel
from robust_library_api.services.utils import (
    model_row_to_dict,
    repository_fallback
)
from robust_library_api.services.author.exc import (
    AuthorNotFoundError, AuthorNotFoundDeletedError, AuthorServiceRepositoryError
)

from robust_library_api.web.api.authors.schema import (
    ResponseAuthor,
    ResponseAuthorCount,
    ResponseAuthorList
)

class AuthorService:
    def __init__(self, author_repository: AuthorRepository):
        self.author_repository: AuthorRepository = author_repository
    
    @repository_fallback(AuthorServiceRepositoryError)
    async def _verify_extract_author(self, author_id: int) -> AuthorModel:
        author_entity = await self.author_repository.get_author_by_id(author_id=author_id)
        if not author_entity:
            raise AuthorNotFoundError(author_id)
        return author_entity

    @repository_fallback(AuthorServiceRepositoryError)
    async def author_creation(self, **author_creation_fields) -> ResponseAuthor:
        created_author = await self.author_repository.create_author(**author_creation_fields)
        return ResponseAuthor(
            message="Author created successfully.",
            data=model_row_to_dict(created_author),
        )

    @repository_fallback(AuthorServiceRepositoryError)
    async def all_authors_list(self) -> ResponseAuthorList:
        all_authors = await self.author_repository.all_authors()
        return ResponseAuthorList(
            message="Authors fetched successfully.",
            data=[model_row_to_dict(author) for author in all_authors],
        )

    @repository_fallback(AuthorServiceRepositoryError)
    async def obtain_author_information(self, author_id: int) -> ResponseAuthor:
        author_entity = await self._verify_extract_author(author_id=author_id)
        return ResponseAuthor(
            message="Author information fetched successfully.",
            data=model_row_to_dict(author_entity),
        )

    @repository_fallback(AuthorServiceRepositoryError)
    async def update_author_information(
        self, author_id: int, **new_author_fields
    ) -> ResponseAuthorCount:
        await self._verify_extract_author(author_id)
        
        new_author_fields_without_nones = {
            field: value
            for field, value in new_author_fields.items()
            if value is not None
        }
        
        update_count = await self.author_repository.update_author_by_id(
            author_to_update_id=author_id, **new_author_fields_without_nones
        )
        return ResponseAuthorCount(
            message=f"{update_count} author(s) updated.",
            data=update_count,
        )

    @repository_fallback(AuthorServiceRepositoryError)
    async def delete_author(self, author_id: int) -> ResponseAuthorCount:
        delete_count = await self.author_repository.delete_author_by_id(author_id=author_id)
        if delete_count == 0:
            raise AuthorNotFoundDeletedError(author_id)
        return ResponseAuthorCount(
            message=f"{delete_count} author(s) deleted.",
            data=delete_count,
        )
