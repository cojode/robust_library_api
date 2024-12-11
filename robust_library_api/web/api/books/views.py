from fastapi import APIRouter, Depends, status

from robust_library_api.container.container import init_container

from robust_library_api.services.book.service import BookService

from robust_library_api.services.book.exc import (
    BookServiceRepositoryError,
    BookNotFoundAuthorError,
    BookNotFoundBookError,
    BookNotFoundDeletedError,
    BookStillObtainsBorrowsError
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
    ResponseBookServiceRepositoryError,
    ResponseBookStillObtainsBorrowsError
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
                        "message": "Book created sucessfully.",
                        "data": {
                            "title": "The Hitchhiker’s Guide to the Galaxy",
                            "description": "42",
                            "author_id": 1,
                            "remaining_amount": 50,
                            "id": 4
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
    """Creates a book entity related to author."""
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
                        "author_id": 1,
                        "id": 1,
                        "title": "sample_book_title",
                        "description": "string",
                        "remaining_amount": 8
                        }
                    ]
                    }
                }
            },
        },
    },
)
async def list_books(book_service: BookService = Depends(get_book_service)):
    """Returns all books in a list."""
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
                    "example":{
                    "status": "success",
                    "message": "Book information fetched successfully.",
                    "data": {
                        "author_id": 1,
                        "id": 4,
                        "title": "The Hitchhiker’s Guide to the Galaxy",
                        "description": "42",
                        "remaining_amount": 50
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
                        "detail": {
                            "status": "fail",
                            "message": "Book with ID 42 not found."
                        }
                    }
                }
            },
        },
    },
)
async def get_book_info(
    id: int, book_service: BookService = Depends(get_book_service)
):
    """
    Returns book rows by its id.
    If id does not match with any existing books, returns 404.
    """
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
        400: {
            "description": "Author not found.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "status": "fail",
                            "message": "Author with ID 0 not found."
                        }
                    }
                }
            }
        },
        404: {
            "description": "Book not found.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "status": "fail",
                            "message": "Book with ID 42 not found."
                        }
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
    """
    Attempts in updating provided book fields.
    If no book with provided id exists, returns 404.
    If no author with provided author_id exists, return 400.
    """
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
            status=status.HTTP_400_BAD_REQUEST,
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
        400: {
            "description": "Book can't be deleted.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "status": "fail",
                            "message": "Can't delete book: Book with ID 1 still has related borrows in table (borrow)."
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
                        "detail": {
                            "status": "error",
                            "message": "Book with ID 42 not found.",
                        }
                    }
                }
            },
        },
    },
)
async def delete_book(
    id: int, book_service: BookService = Depends(get_book_service)
):
    """
    Attempts to delete a book by its id.
    If no book is matched with provided id, returns 404.
    If there are any borrows related with deleted book, deletion is prevented with 400.
    """
    try:
        await book_service.delete_book(id)
    except BookNotFoundDeletedError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_404_NOT_FOUND,
            response_model=ResponseBookNotFoundBook
        )
    except BookStillObtainsBorrowsError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_400_BAD_REQUEST,
            response_model=ResponseBookStillObtainsBorrowsError
        )
    except BookServiceRepositoryError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response_model=ResponseBookServiceRepositoryError
        )
