import enum

from pydantic import BaseModel, Field
from typing import Optional, Any, List

class ResponseStatus(str, enum.Enum):
    success = "success"
    fail = "fail"
    error = "error"

class StandardResponse(BaseModel):
    status: ResponseStatus
    message: str

class StandardSuccessResponse(StandardResponse):
    status: ResponseStatus = ResponseStatus.success
    data: Optional[Any] = None
    
class StandardSuccessListResponse(StandardSuccessResponse):
    data: Optional[List[dict]] = None

class StandardSuccessCountResponse(StandardSuccessResponse):
    data: Optional[int] = None

class StandardFailResponse(StandardResponse):
    status: ResponseStatus = ResponseStatus.fail

class StandardServiceRepositoryErrorResponse(StandardResponse):
    status: ResponseStatus = ResponseStatus.error
