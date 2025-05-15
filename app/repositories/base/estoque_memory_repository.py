from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel
from app.common.datetime import utcnow
from app.common.exceptions import NotFoundException
from app.repositories.base import AsyncCrudRepository

T = TypeVar("T", bound=BaseModel)
ID = TypeVar("ID", bound=int | str)

class AsyncMemoryRepository(AsyncCrudRepository[T, ID], Generic[T, ID]):

    def __init__(self):
        super().__init__()
        self.memory = []

    async def create(self, entity: T) -> T:
        entity_dict = entity.model_dump(by_alias=True)
        entity_dict["created_at"] = utcnow()
        self.memory.append(entity)
        return entity_dict

    async def find_by_id(self, entity_id: ID) -> Optional[T]:
        result = next((r for r in self.memory if r.identity == entity_id), None)
        if result:
            return result
        raise NotFoundException(f"Registro com ID {entity_id} não encontrado")

    async def find(self, seller_id: Optional[str] = None, sku: Optional[str] = None, limit: int = 10, offset: int = 0) -> List[T]:
        filtered_list = self.memory

        if seller_id:
            filtered_list = [item for item in filtered_list if item.seller_id == seller_id]
        if sku:
            filtered_list = [item for item in filtered_list if item.sku == sku]

        # Paginação
        return filtered_list[offset:offset + limit]

    async def update(self, entity_id: ID, entity: Any) -> T:
        entity_dict = entity.model_dump(by_alias=True, exclude={"identity"})
        entity_dict["updated_at"] = utcnow()

        current_document = await self.find_by_id(entity_id)
        if current_document:
            return T(**entity_dict)
        raise NotFoundException(f"Registro com ID {entity_id} não encontrado")

    async def delete_by_id(self, entity_id: ID) -> None:
        current_document = await self.find_by_id(entity_id)
        if not current_document:
            raise NotFoundException(f"Registro com ID {entity_id} não encontrado")
        self.memory.remove(current_document)
