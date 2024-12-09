from abc import ABC, abstractmethod
from typing import Type, TypeVar, List, Optional, Any, Dict, Generic
from sqlalchemy import select as sql_select, update as sql_update, delete as sql_delete, Select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .exc import (
    RepositoryError
)

T = TypeVar("T")


class AbstractCRUDRepository(ABC, Generic[T]):
    @abstractmethod
    async def create(self, entity: Optional[T] = None, **kwargs: Any) -> T:
        """
        Creates an entity, either using the provided instance or from keyword arguments.

        :param entity: Optional instance of the model to create.
        :param kwargs: Additional fields to create a new instance if entity is not provided.
        :return: The created instance of the entity.
        :raises UniqueConstraintViolationError: If a unique constraint is violated.
        :raises RepositoryError: If the creation fails due to other database issues.
        """
        pass

    @abstractmethod
    async def read(
        self, only_first=False, limit: Optional[int] = None, 
        offset: Optional[int] = None, order_by=None, **filters: Any
    ) -> List[T]:
        """
        Reads entities with an optional QueryBuilder for custom filtering.
        By default reads all entries, alter only_first flag to read only first entry.


        :return: List of entities matching the conditions.
        :raises RepositoryError: If the read operation fails.
        """
        pass

    @abstractmethod
    async def update(
        self, fields: Dict[str, Any], **filters: Any
    ) -> int:
        """
        Updates entities based on conditions set in QueryBuilder and specified fields.


        :param fields: Fields to update in the matching entities.
        :return: Number of rows affected by the update.
        :raises ValueError: If no fields are provided for updating.
        :raises RepositoryError: If the update operation fails.
        """
        pass

    @abstractmethod
    async def delete(self, entity: Optional[T] = None, **filters: Any) -> int:
        """
        Deletes entities based on conditions set in QueryBuilder.


        :return: Number of rows affected by the delete operation.
        :raises RepositoryError: If the delete operation fails.
        """
        pass

    @abstractmethod
    async def save(self, entity: T) -> T:
        """
        Saves (inserts or updates) the provided entity in the database.

        :param entity: The entity instance to be saved.
        :return: The saved instance of the entity.
        :raises RepositoryError: If the save operation fails.
        """
        pass

T = TypeVar("T")

class CRUDRepository(AbstractCRUDRepository[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def create(self, entity: Optional[T] = None, **kwargs: Any) -> T:
        try:
            instance = entity if entity else self.model(**kwargs)
            self.session.add(instance)
            await self.session.flush([instance])
            return instance
        except SQLAlchemyError as e:
            raise RepositoryError(f"Failed to create entity: {e}") from e

    async def read(
        self, only_first=False, raw_query: Select = None, limit: Optional[int] = None, 
        offset: Optional[int] = None, order_by=None, **filters: Any
    ) -> List[T]:
        """
        Reads entities with optional filters, pagination, and ordering.
        """
        try:
            query = sql_select(self.model).filter_by(**filters)
            if order_by is not None:
                query = query.order_by(order_by)
            if limit is not None:
                query = query.limit(limit)
            if offset is not None:
                query = query.offset(offset)
            
            if raw_query is not None:
                query = raw_query

            result = await self.session.execute(query)
            result_scalars = result.scalars()
            return result_scalars.first() if only_first else result_scalars.all()

        except SQLAlchemyError as e:
            raise RepositoryError(f"Failed to read entities: {e}") from e

    async def update(self, fields: Dict[str, Any], **filters: Any) -> int:
        """
        Updates entities based on conditions provided in filters and fields to update.
        """
        if not fields:
            raise ValueError("No fields provided to update")
        try:
            query = sql_update(self.model).values(**fields).filter_by(**filters)
            result = await self.session.execute(query)
            await self.session.commit()
            return result.rowcount
        except SQLAlchemyError as e:
            raise RepositoryError(f"Failed to update entities: {e}") from e

    async def delete(self, entity: Optional[T] = None, **filters: Any) -> int:
        """
        Deletes entities based on conditions set in filters.
        """
        try:
            if entity is not None:
                await self.session.delete(entity)
                return 1
            
            query = sql_delete(self.model).filter_by(**filters)
            result = await self.session.execute(query)
            await self.session.commit()
            return result.rowcount
        except SQLAlchemyError as e:
            raise RepositoryError(f"Failed to delete entities: {e}") from e

    async def save(self, entity: T) -> T:
        """
        Saves (inserts or updates) the provided entity in the database.
        """
        try:
            self.session.add(entity)
            await self.session.flush()
            await self.session.refresh(entity)
            return entity
        except SQLAlchemyError as e:
            raise RepositoryError(f"Failed to save entity: {e}") from e