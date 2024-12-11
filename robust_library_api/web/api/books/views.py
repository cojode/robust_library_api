from fastapi import APIRouter, Depends, status

from robust_library_api.services.book.service import BookService
from robust_library_api.container.container import init_container

from robust_library_api.web.api.books.schema import (
    BookCreateRequest, 
    BookUpdateRequest,
    BookListResponse,
    BookResponse,
    BookCountResponse
)

router = APIRouter()

async def get_book_service(
    container=Depends(init_container)
) -> BookService:
    return container.resolve(BookService)


@router.post(
    "/books",
    status_code=status.HTTP_201_CREATED,
    response_model=BookResponse,
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
    data: BookCreateRequest,
    book_service: BookService = Depends(get_book_service),
):
    return await book_service.book_creation(**dict(data)) 


@router.get(
    "/books",
    status_code=status.HTTP_200_OK,
    response_model=BookListResponse,
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
    return await book_service.all_books_list()


@router.get(
    "/books/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model=BookResponse,
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
    book_id: int, book_service: BookService = Depends(get_book_service)
):
    return await book_service.obtain_book_information(book_id)


@router.put(
    "/books/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model=BookCountResponse,
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
    book_id: int,
    new_book_fields: BookUpdateRequest,
    book_service: BookService = Depends(get_book_service),
):
    return await book_service.update_book_information(
        book_id, **dict(new_book_fields)
    )


@router.delete(
    "/books/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model=BookCountResponse,
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
    book_id: int, book_service: BookService = Depends(get_book_service)
):
    return await book_service.delete_book(book_id)
