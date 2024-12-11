from pydantic import BaseModel, Field
from typing import Optional, Any, List

class BookCreateRequest(BaseModel):
    title: str = Field(..., max_length=200)
    description: str = Field(..., max_length=1024)
    author_id: int = Field(...)
    remaining_amount: int = Field(...)

class BookUpdateRequest(BaseModel):
    title: Optional[str] = Field(..., max_length=200)
    description: Optional[str] = Field(..., max_length=1024)
    author_id: Optional[int] = Field(...)
    remaining_amount: Optional[int] = Field(...)

class BookResponse(BaseModel):
    status: str
    message: str
    data: Optional[Any] = None


class BookListResponse(BookResponse):
    data: Optional[List[dict]] = None


class BookCountResponse(BookResponse):
    data: Optional[int] = None