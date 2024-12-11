from robust_library_api.web.api.schema import StandardResponse

from fastapi import HTTPException, status

def raise_http_exception_with_model_response(exc_from: Exception, status: status, response_model: StandardResponse):
    raise HTTPException(
            status,
            detail=response_model(
                message=exc_from.message,
            ).model_dump()
        )