"""
Container initialization module.

This module contains functions to initialize container for application.

Initialization of container consists of registration of all application services
and repositories. All registrations are done in singleton scope.

"""
from functools import lru_cache

from punq import Container, Scope

from robust_library_api.db.repositories.author import AuthorRepository
from robust_library_api.db.repositories.book import BookRepository
from robust_library_api.db.repositories.borrow import BorrowRepository

from robust_library_api.db.database import Database

from robust_library_api.settings import settings

@lru_cache(1)
def init_container() -> Container:
    """
    Initialize container for application.

    This function uses lru_cache decorator to cache result of container
    initialization. This means that first call to this function will initialize
    container and subsequent calls will return cached result.

    :return: Initialized container.
    :rtype: Container
    """
    return _init_container()

def _init_container() -> Container:
    """
    Initialize container for application.

    This function registers all services and repositories in container.

    :return: Initialized container.
    :rtype: Container
    """
    container = Container()
    container.register(
        Database, scope=Scope.singleton,
        factory=lambda: Database(
            url=str(settings.db_url),
        ))

    container.register(AuthorRepository)
    container.register(BookRepository)
    container.register(BorrowRepository)

    from robust_library_api.services.author.service import AuthorService
    container.register(
        AuthorService, scope=Scope.singleton
    )
    
    from robust_library_api.services.book.service import BookService
    container.register(
        BookService, scope=Scope.singleton
    )

    return container
