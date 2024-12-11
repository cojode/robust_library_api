from fastapi.routing import APIRouter

from robust_library_api.web.api import (
    monitoring,
    authors,
    books
)

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(authors.router)
api_router.include_router(books.router)
