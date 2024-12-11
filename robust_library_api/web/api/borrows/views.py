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
                        "message": "Borrow created successfully.",
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
async def create_borrow(
    data: RequestBorrowCreate,
    borrow_service: BorrowService = Depends(get_borrow_service),
):
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
async def list_borrows(borrow_service: BorrowService = Depends(get_borrow_service)):
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
            "description": "Borrow not found.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Borrow with ID 42 not found.",
                        "data": None
                    }
                }
            },
        },
    },
)
async def get_borrow_info(
    id: int, borrow_service: BorrowService = Depends(get_borrow_service)
):
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
        404: {
            "description": "Borrow not found.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Borrow with ID 42 not found.",
                        "data": None
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
    try:
        await borrow_service.close_borrow(borrow_id=id)
    except BorrowAlreadyClosedError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_400_BAD_REQUEST,
            response_model=ResponseBorrowAlreadyClosed
        )
    except BorrowServiceRepositoryError as e:
        raise_http_exception_with_model_response(
            exc_from=e,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            response_model=ResponseBorrowServiceRepositoryError
        )