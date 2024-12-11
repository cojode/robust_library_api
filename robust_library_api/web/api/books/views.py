from fastapi import APIRouter, Depends, status

from robust_library_api.container.container import init_container

from robust_library_api.services.book.service import BookService

from robust_library_api.services.book.exc import (
    BookServiceRepositoryError,
    BookNotFoundAuthorError,
    BookNotFoundBookError,
    BookNotFoundDeletedError,
)


from robust_library_api.web.api.utils import raise_http_exception_with_model_response

from robust_library_api.web.api.books.schema import (
    RequestBookCreate, 
    RequestBookUpdate,
    ResponseBook,
    ResponseBookCount,
    ResponseBookList,
    ResponseBookNotFoundBook,
    ResponseBookNotFoundAuthor,
    ResponseBookServiceRepositoryError
)

router = APIRouter()

async def get_book_service(
    container=Depends(init_container)
) -> BookService:
    return container.resolve(BookService)


@router.post(
    "/books",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseBook,
    responses={
        201: {
            "description": "Book created successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Book created successfully.",
                        "data": {
                            "id": 1,
                            "title": "John",
                            "description": "Doe",
                            "author_id": 1,
                            "remaining_amount": 42
                        }
                    }
                }
            },
        },
    },
)
async def create_book(
    data: RequestBookCreate,
    book_service: BookService = Depends(get_book_service),
):
    try:
        return await book_service.book_creation(**dict(data))
    except BookNotFoundAuthorError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_404_NOT_FOUND,
            response_model=ResponseBookNotFoundAuthor
        )
    except BookServiceRepositoryError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response_model=ResponseBookServiceRepositoryError
        )
        


@router.get(
    "/books",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBookList,
    responses={
        200: {
            "description": "List of books fetched successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Books fetched successfully.",
                        "data": [
                            {
                            "id": 1,
                            "title": "John",
                            "description": "Doe",
                            "author_id": 1,
                            "remaining_amount": 42
                            }
                        ]
                    }
                }
            },
        },
    },
)
async def list_books(book_service: BookService = Depends(get_book_service)):
    try:
        return await book_service.all_books_list()
    except BookServiceRepositoryError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response_model=ResponseBookServiceRepositoryError
        )

@router.get(
    "/books/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBook,
    responses={
        200: {
            "description": "Book information fetched successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Book information fetched successfully.",
                        "data": {
                            "id": 1,
                            "title": "John",
                            "description": "Doe",
                            "author_id": 1,
                            "remaining_amount": 42
                        }
                    }
                }
            },
        },
        404: {
            "description": "Book not found.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Book with ID 42 not found.",
                        "data": None
                    }
                }
            },
        },
    },
)
async def get_book_info(
    id: int, book_service: BookService = Depends(get_book_service)
):
    try:
        return await book_service.obtain_book_information(id)
    except BookNotFoundBookError as e:
        raise raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_404_NOT_FOUND,
            response_model=ResponseBookNotFoundBook
        )
    except BookServiceRepositoryError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response_model=ResponseBookServiceRepositoryError
        )


@router.put(
    "/books/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBookCount,
    responses={
        200: {
            "description": "Book information updated successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "1 book updated successfully.",
                        "data": 1
                    }
                }
            },
        },
        404: {
            "description": "Book not found.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Book with ID 42 not found.",
                        "data": None
                    }
                }
            },
        },
    },
)
async def update_book(
    id: int,
    new_book_fields: RequestBookUpdate,
    book_service: BookService = Depends(get_book_service),
):
    try:
        return await book_service.update_book_information(
            id, **dict(new_book_fields)
        )
    except BookNotFoundBookError as e:
        raise raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_404_NOT_FOUND,
            response_model=ResponseBookNotFoundBook
        )
    except BookNotFoundAuthorError as e:
        raise raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_404_NOT_FOUND,
            response_model=ResponseBookNotFoundAuthor
        )
    except BookServiceRepositoryError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response_model=ResponseBookServiceRepositoryError
        )

@router.delete(
    "/books/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        200: {
            "description": "Book deleted successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "1 book deleted successfully.",
                        "data": 1
                    }
                }
            },
        },
        404: {
            "description": "Book not found.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Book with ID 42 not found.",
                        "data": None
                    }
                }
            },
        },
    },
)
async def delete_book(
    id: int, book_service: BookService = Depends(get_book_service)
):
    try:
        await book_service.delete_book(id)
    except BookNotFoundDeletedError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_404_NOT_FOUND,
            response_model=ResponseBookNotFoundBook
        )
    except BookServiceRepositoryError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response_model=ResponseBookServiceRepositoryError
        )
