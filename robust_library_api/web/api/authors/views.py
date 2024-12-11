from fastapi import APIRouter, Depends, status

from robust_library_api.services.author.service import AuthorService
from robust_library_api.services.author.exc import (
    AuthorNotFoundError, 
    AuthorNotFoundDeletedError,
    AuthorServiceRepositoryError,
    AuthorStillObtainsBooksError
)

from robust_library_api.container.container import init_container

from robust_library_api.web.api.utils import raise_http_exception_with_model_response

from robust_library_api.web.api.authors.schema import (
    RequestAuthorCreate,
    RequestAuthorUpdate,
    ResponseAuthor,
    ResponseAuthorCount,
    ResponseAuthorList,
    ResponseAuthorNotFound,
    ResponseAuthorServiceRepositoryError,
    ResponseAuthorStillObtainsBooks,
)

router = APIRouter()

async def get_author_service(
    container=Depends(init_container)
) -> AuthorService:
    return container.resolve(AuthorService)


@router.post(
    "/authors",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseAuthor,
    responses={
        201: {
            "description": "Author created successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Author created successfully.",
                        "data": {
                            "id": 1,
                            "name": "John",
                            "surname": "Doe",
                            "birth_date": "11.11.1990"
                        }
                    }
                }
            },
        },
    },
)
async def create_author(
    data: RequestAuthorCreate,
    author_service: AuthorService = Depends(get_author_service),
):  
    """
    Creates new author.
    """
    try:
        return await author_service.author_creation(**dict(data))
    except AuthorServiceRepositoryError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response_model=ResponseAuthorServiceRepositoryError
        )
        


@router.get(
    "/authors",
    status_code=status.HTTP_200_OK,
    response_model=ResponseAuthorList,
    responses={
        200: {
            "description": "List of authors fetched successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Authors fetched successfully.",
                        "data": [
                            {"id": 1, "name": "John", "surname": "Doe", "birth_date": "11.11.990"},
                        ]
                    }
                }
            },
        },
    },
)
async def list_authors(author_service: AuthorService = Depends(get_author_service)):
    """
    Returns all authors in list.
    """
    try:
        return await author_service.all_authors_list()
    except AuthorServiceRepositoryError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response_model=ResponseAuthorServiceRepositoryError
        )


@router.get(
    "/authors/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseAuthor,
    responses={
        200: {
            "description": "Author information fetched successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Author information fetched successfully.",
                        "data": {
                            "id": 1,
                            "name": "John",
                            "surname": "Doe",
                            "birth_date": "11.11.1990"
                        }
                    }
                }
            },
        },
        404: {
            "description": "Author not found.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Author with ID 42 not found.",
                        "data": None
                    }
                }
            },
        },
    },
)
async def get_author_info(
    id: int, author_service: AuthorService = Depends(get_author_service)
): 
    """
    Gathers information about sepcific author by related id.
    If no author found with provided id, returns 404.
    """
    try:
        return await author_service.obtain_author_information(author_id=id)
    except AuthorNotFoundError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_404_NOT_FOUND,
            response_model=ResponseAuthorNotFound      
        )
    except AuthorServiceRepositoryError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response_model=ResponseAuthorServiceRepositoryError
        )

@router.put(
    "/authors/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseAuthorCount,
    responses={
        200: {
            "description": "Author information updated successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "1 author(s) updated successfully.",
                        "data": 1
                    }
                }
            },
        },
        404: {
            "description": "Author not found.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Author with ID 42 not found.",
                        "data": None
                    }
                }
            },
        },
    },
)
async def update_author(
    id: int,
    new_author_fields: RequestAuthorUpdate,
    author_service: AuthorService = Depends(get_author_service),
):
    """
    Updates author entry with provided fields.
    If no author found with provided id, returns 404.
    """
    try:
        return await author_service.update_author_information(
            author_id=id, **dict(new_author_fields)
        )
    except AuthorNotFoundError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_404_NOT_FOUND,
            response_model=ResponseAuthorNotFound      
        )
    except AuthorServiceRepositoryError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response_model=ResponseAuthorServiceRepositoryError
        )


@router.delete(
    "/authors/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        200: {
            "description": "Author deleted successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "1 author deleted successfully.",
                        "data": 1
                    }
                }
            },
        },
        404: {
            "description": "Author not found.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Author with ID 42 not found.",
                        "data": None
                    }
                }
            },
        },
    },
)
async def delete_author(
    id: int, author_service: AuthorService = Depends(get_author_service)
):
    """
    Deletes an author from database.
    If no author were deleted, returns 404.
    If there are any books with deleted author, deletion is prevented with 400.
    """
    try:
        await author_service.delete_author(author_id=id)
    except AuthorNotFoundDeletedError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_404_NOT_FOUND,
            response_model=ResponseAuthorNotFound
        )
    except AuthorStillObtainsBooksError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_400_BAD_REQUEST,
            response_model=ResponseAuthorStillObtainsBooks
        )
    except AuthorServiceRepositoryError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response_model=ResponseAuthorServiceRepositoryError
        )