from pydantic import BaseModel, Field
from typing import Optional

from datetime import date

from robust_library_api.web.api.schema import (
    StandardSuccessResponse,
    StandardSuccessListResponse,
    StandardSuccessCountResponse,
    StandardFailResponse,
    StandardServiceRepositoryErrorResponse
)

class RequestAuthorCreate(BaseModel):
    name: str = Field(..., max_length=200)
    surname: str = Field(..., max_length=200)
    birth_date: date = Field(...)

class RequestAuthorUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=200)
    surname: Optional[str] = Field(default=None, max_length=200)
    birth_date: Optional[date] = Field(default=None)
    
    class Config:
        extra = "forbid"

class ResponseAuthor(StandardSuccessResponse): ...
        
class ResponseAuthorList(StandardSuccessListResponse): ...
class ResponseAuthorCount(StandardSuccessCountResponse): ...

class ResponseAuthorNotFound(StandardFailResponse): ...
class ResponseAuthorServiceRepositoryError(StandardServiceRepositoryErrorResponse): ...