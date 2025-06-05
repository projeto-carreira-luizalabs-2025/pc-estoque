from uuid import UUID

from app.api.common.schemas.pagination import Paginator
<<<<<<< HEAD:app/services/estoque/estoque_service.py

from app.services.estoque.estoque_exceptions import EstoqueAlreadyExistsException
from ...models.estoque_model import Estoque
from ...repositories.estoque_repository import EstoqueRepository
from ..base import CrudService
=======
from ..models.estoque_model import Estoque
from ..repositories.estoque_repository import EstoqueRepository
from .base import CrudService
>>>>>>> v2.2:app/services/estoque_service.py


class EstoqueServices(CrudService[Estoque, UUID]):
    def __init__(self, repository: EstoqueRepository):
        super().__init__(repository)
        self.repository: EstoqueRepository = repository 

    async def find_by_seller_id_and_sku(self, seller_id: str, sku: str) -> Estoque:
        """
        Busca um estoque pelo seller_id e SKU.
        """
        return await self.repository.find_by_seller_id_and_sku(seller_id=seller_id, sku=sku)

    async def create(self, estoque: Estoque) -> Estoque:
        """
        Cria um novo estoque.
        """
        existing = await self.repository.find_by_seller_id_and_sku(seller_id=estoque.seller_id, sku=estoque.sku)
        if existing:
            raise EstoqueAlreadyExistsException()
        
        return await self.repository.create(estoque)

    async def update(self, seller_id: str, sku: str, estoque_update) -> Estoque:
<<<<<<< HEAD:app/services/estoque/estoque_service.py
        from app.api.v1.schemas.estoque_schema import EstoqueUpdate        
=======
        from app.api.v1.schemas.estoque_schema import EstoqueUpdate 

>>>>>>> v2.2:app/services/estoque_service.py

        """
        Atualiza um estoque existente.
        """
        if not isinstance(estoque_update, EstoqueUpdate):
            raise TypeError("So é permitido atualizar a quantidade do estoque")
        return await self.repository.update(seller_id=seller_id, sku=sku, quantidade=estoque_update.quantidade)

    async def delete(self, seller_id: str, sku: str) -> None:
        """
        Deleta um estoque existente.
        """
        estoque = await self.repository.find_by_seller_id_and_sku(seller_id=seller_id, sku=sku)

        return await self.repository.delete(item_id=estoque.id)

    async def list(self, paginator: Paginator, filters: dict) -> list[Estoque]:
        """
        Lista todos os estoques.
        """
        resultados_filtrados = await self.repository.find(filters, limit=paginator.limit, offset=paginator.offset)
        return resultados_filtrados