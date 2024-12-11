from fastapi import APIRouter, Depends, status

from robust_library_api.container.container import init_container

from robust_library_api.services.borrow.service import BorrowService

from robust_library_api.services.borrow.exc import (
    BorrowServiceRepositoryError,
    BorrowNotFoundBookError,
    BorrowNotFoundBorrowError,
    BorrowBookExhaustedError,
    BorrowAlreadyClosedError
)


from robust_library_api.web.api.utils import raise_http_exception_with_model_response

from robust_library_api.web.api.borrows.schema import (
    RequestBorrowCreate, 
    ResponseBorrow,
    ResponseBorrowList,
    ResponseBorrowNotFoundBorrow,
    ResponseBorrowNotFoundBook,
    ResponseBorrowBookExhausted,
    ResponseBorrowAlreadyClosed,
    ResponseBorrowServiceRepositoryError,
)

router = APIRouter()

async def get_borrow_service(
    container=Depends(init_container)
) -> BorrowService:
    return container.resolve(BorrowService)


@router.post(
    "/borrows",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseBorrow,
    responses={
        201: {
            "description": "Borrow created successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Borrow created sucessfully.",
                        "data": {
                            "book_id": 4,
                            "reader_name": "string",
                            "date_of_issue": "2024-12-11",
                            "id": 5
                        }
                    }
                }
            },
        },
        404: {
            "description": "Borrow created successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                                "status": "fail",
                                "message": "Book with ID 999 not found."
                        }
                    }
                }
            },
        },
        400: {
            "description": "Borrow created successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                                "status": "fail",
                                "message": "Can't borrow: book with ID 1 are over - no book left."
                        }
                    }
                }
            },
        },
    },
)
async def create_borrow(
    data: RequestBorrowCreate,
    borrow_service: BorrowService = Depends(get_borrow_service),
):
    """
    Creates a borrow entity.
    Related book entity would lose a book balance (remaining_amount).
    Returns 404 if related book id does not match with any of existing books.
    Returns 400 if related book balance is exhausted(equals 0).
    """
    try:
        return await borrow_service.borrow_creation(**dict(data))
    except BorrowNotFoundBookError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_404_NOT_FOUND,
            response_model=ResponseBorrowNotFoundBook
        )
    except BorrowBookExhaustedError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_400_BAD_REQUEST,
            response_model=ResponseBorrowBookExhausted
        )
    except BorrowServiceRepositoryError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response_model=ResponseBorrowServiceRepositoryError
        )
        


@router.get(
    "/borrows",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBorrowList,
    responses={
        200: {
            "description": "List of borrows fetched successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Borrows fetched successfully.",
                        "data": [
                    {
                        "date_of_issue": "2024-12-11",
                        "id": 3,
                        "reader_name": "abyss",
                        "date_of_return": None,
                        "book_id": 1
                    },
                    {
                        "date_of_issue": "2024-12-11",
                        "id": 1,
                        "reader_name": "abyss",
                        "date_of_return": "2024-12-11",
                        "book_id": 1
                    }, 
                ]
                    }
                }
            },
        },
    },
)
async def list_borrows(borrow_service: BorrowService = Depends(get_borrow_service)):
    """
    Returns all borrows in a list.
    """
    try:
        return await borrow_service.all_borrows_list()
    except BorrowServiceRepositoryError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response_model=ResponseBorrowServiceRepositoryError
        )

@router.get(
    "/borrows/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBorrow,
    responses={
        200: {
            "description": "Borrow information fetched successfully.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Borrow information fetched successfully.",
                        "data": {
                            "date_of_issue": "2024-12-11",
                            "id": 2,
                            "reader_name": "string",
                            "date_of_return": "2024-12-11",
                            "book_id": 1
                        }
                    }
                }
            },
        },
        404: {
            "description": "Borrow not found.",
            "content": {
                "application/json": {
                    "example":{
                        "detail": {
                            "status": "fail",
                            "message": "Borrow with ID 8888 not found."
                        }
                    }
                }
            },
        },
    },
)
async def get_borrow_info(
    id: int, borrow_service: BorrowService = Depends(get_borrow_service)
):
    """
    Obtains borrow information by its id.
    If no borrow matches with provided id, returns 404.
    """
    try:
        return await borrow_service.obtain_borrow_information(id)
    except BorrowNotFoundBorrowError as e:
        raise raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_404_NOT_FOUND,
            response_model=ResponseBorrowNotFoundBorrow
        )
    except BorrowServiceRepositoryError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response_model=ResponseBorrowServiceRepositoryError
        )

@router.patch(
    "/borrows/{id}/return",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {
            "description": "Borrow closed",
            "content": {
                "application/json": {
                    "example": {}
                }
            },
        },
        400: {
            "description": "Borrow not found.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "status": "fail",
                            "message": "Can't close borrow: borrow with ID 1 already closed."
                        }
                    }
                }
            },
        },
    },
)
async def return_borrow(
    id: int,
    borrow_service: BorrowService = Depends(get_borrow_service)
):
    """
    Patch to borrow entity representing returning a book from a borrow.
    Returns 400 if borrow was already closed before.
    Else returns 204, and if borrow with provided id really exists:
    1) Appends field with request date 
    2) Appends book balance of related book entity on 1
    """
    try:
        await borrow_service.close_borrow(borrow_id=id)
    except BorrowAlreadyClosedError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_400_BAD_REQUEST,
            response_model=ResponseBorrowAlreadyClosed
        )
    except BorrowNotFoundBorrowError:
        pass
    except BorrowServiceRepositoryError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response_model=ResponseBorrowServiceRepositoryError
        )