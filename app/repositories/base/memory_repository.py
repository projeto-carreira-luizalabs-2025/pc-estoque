from typing import Any, Generic, List, Optional, TypeVar, Type
from uuid import UUID
from pydantic import BaseModel
from app.common.datetime import utcnow
from app.common.exceptions import NotFoundException
from .async_crud_repository import AsyncCrudRepository

T = TypeVar("T", bound=BaseModel)
ID = TypeVar("ID", bound=int | str | UUID)


class AsyncMemoryRepository(AsyncCrudRepository[T, ID], Generic[T, ID]):

    def __init__(self, key_name: str, model_class: Type[T]):
        super().__init__()
        self.key_name = key_name
        self.memory: List[dict] = []
        self.model_class = model_class

    async def create(self, entity: T) -> T:
        entity_dict = entity.model_dump(by_alias=True)
        entity_dict["created_at"] = utcnow()        
        self.memory.append(entity_dict)

        return entity

    async def find_by_id(self, entity_id: ID) -> T:
        # XXX Lembrar que elementos da memória são dicionionários
        result = next((r for r in self.memory if r.get(self.key_name) == entity_id), None)
        if result is not None:
            result = self.model_class(**result)
        return result
    
    @staticmethod
    def _can_filter(data: T, filters: dict | None) -> bool:
        filters = filters or {}

        for key, value in filters.items():
            if value is not None and data.get(key) != value:
                return False
        return True

    async def find(
        self,
        filters: dict,
        limit: int = 10,
        offset: int = 0,
        sort: Optional[dict] = None
    ) -> List[T]:
        filtered_list = [data for data in self.memory if self._can_filter(data, filters)]
        result_list = [self.model_class(**register) for register in filtered_list]
        return result_list

    async def update(self, entity_id: ID, entity: T) -> T:
       # XXX Chave fixada por somehting, ajustar depois.
        entity_dict = entity.model_dump(by_alias=True, exclude={"identity"})
        entity_dict["updated_at"] = utcnow()

        current_document = await self.find_by_id(entity_id)

        if current_document:
            # TODO XXX Atualizar os dados
            return self.model_class(**current_document)
        raise NotFoundException()

    async def delete_by_id(self, entity_id: ID) -> None:
        # XXX TODO
        current_document = await self.find_by_id(entity_id)
        if not current_document:
            raise NotFoundException()

