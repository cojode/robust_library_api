from pydantic import BaseModel, Field
from typing import Optional

from robust_library_api.web.api.schema import (
    StandardSuccessResponse,
    StandardSuccessListResponse,
    StandardSuccessCountResponse,
    StandardFailResponse,
    StandardServiceRepositoryErrorResponse
)

class RequestBookCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: str = Field(..., max_length=1024)
    author_id: int = Field(...)
    remaining_amount: int = Field(..., gt=0)

class RequestBookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1024)
    author_id: Optional[int] = Field(default=None)
    remaining_amount: Optional[int] = Field(default=None, gt=0, le=20000)

class ResponseBook(StandardSuccessResponse): ...

class ResponseBookList(StandardSuccessListResponse): ...
class ResponseBookCount(StandardSuccessCountResponse): ...

class ResponseBookNotFoundBook(StandardFailResponse): ...
class ResponseBookNotFoundAuthor(StandardFailResponse): ...
class ResponseBookStillObtainsBorrowsError(StandardFailResponse): ...

class ResponseBookServiceRepositoryError(StandardServiceRepositoryErrorResponse): ...