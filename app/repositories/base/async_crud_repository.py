from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")
ID = TypeVar("ID")


class AsyncCrudRepository(ABC, Generic[T, ID]):
    """
    Interface genérica para operações de repositório CRUD.
    """

    @abstractmethod
    async def create(self, entity: T) -> T:
        """
        Salva uma entidade no repositório.
        """

    @abstractmethod
    async def find_by_id(self, entity_id: ID) -> T | None:
        """
        Busca uma entidade pelo seu identificador único.
        """

    @abstractmethod
    async def find(self, filters: dict, limit: int, offset: int, sort: dict | None = None) -> list[T]:
        """
        Busca entidades no repositório, utilizando filtros e paginação.
        """

    @abstractmethod
    async def update(self, entity_id: ID, entity: Any) -> T:
        """
        Atualiza uma entidade existente no repositório.
        """

    @abstractmethod
    async def delete_by_id(self, entity_id: ID) -> None:
        """
        Remove uma entidade pelo seu identificador único.
        """
