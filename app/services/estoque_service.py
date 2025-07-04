from app.api.common.schemas.pagination import Paginator
from app.common.datetime import utcnow
from app.common.exceptions.estoque_exceptions import EstoqueBadRequestException, EstoqueNotFoundException
from ..models.estoque_model import Estoque
from .base import CrudService
from ..repositories.estoque_repository import EstoqueRepository

from pclogging import LoggingBuilder

LoggingBuilder.init(log_level="DEBUG")

logger = LoggingBuilder.get_logger(__name__)
class EstoqueServices(CrudService[Estoque, str]):

    repository: EstoqueRepository
    
    def __init__(self, repository: EstoqueRepository):
        super().__init__(repository)

    async def get_by_seller_id_and_sku(self, seller_id: str, sku: str) -> Estoque:
        """
        Busca um estoque pelo seller_id e SKU.
        """
        logger.debug(f"Buscando estoque para seller_id={seller_id}, sku={sku}")
        estoque = await self.repository.find_by_seller_id_and_sku(seller_id, sku)

        self._raise_not_found(seller_id, sku, estoque is None)
        return Estoque.model_validate(estoque)

    async def create(self, estoque: Estoque) -> Estoque:
        """
        Cria um novo estoque.
        """
        logger.info(f"Criando novo estoque para seller_id={estoque.seller_id}, sku={estoque.sku}")
        await self._validate_non_existent_estoque(estoque.seller_id, estoque.sku)
        self._validate_positive_estoque(estoque)

        estoque = Estoque(**estoque.model_dump())
        created = await super().create(estoque)
        logger.debug(f"Estoque criado com sucesso: {created}")
        return created

    async def update(self, seller_id: str, sku: str, quantidade: int) -> Estoque:
        """
        Atualiza um estoque existente, modificando apenas a quantidade.

        Recebe: seller_id, sku e quantidade.
        """
        logger.info(f"Atualizando estoque seller_id={seller_id}, sku={sku} para quantidade={quantidade}")
        estoque_found = await self.repository.find_by_seller_id_and_sku(seller_id, sku)
        self._raise_not_found(seller_id, sku, estoque_found is None)
        
        temp_estoque = Estoque(**(dict(estoque_found) if isinstance(estoque_found, dict) else estoque_found.model_dump()))
        temp_estoque.quantidade = quantidade
        self._validate_positive_estoque(temp_estoque)
        
        updated_data = temp_estoque.model_dump()
        updated_data["updated_at"] = utcnow()
        
        updated_entity = Estoque(**updated_data)
        updated = await self.repository.update_by_seller_id_and_sku(seller_id, sku, updated_entity)
        logger.debug(f"Estoque atualizado: {updated}")
        return updated

    async def delete(self, seller_id: str, sku: str):
        """
        Deleta um estoque existente.
        """
        logger.info(f"Deletando estoque seller_id={seller_id}, sku={sku}")
        estoque_found = await self.repository.find_by_seller_id_and_sku(seller_id, sku)
        self._raise_not_found(seller_id, sku, estoque_found is None)
        deleted = await self.repository.delete_by_seller_id_and_sku(seller_id, sku)
        if not deleted:
            logger.error(f"Erro ao deletar estoque seller_id={seller_id}, sku={sku}")
            self._raise_bad_request(
                message="Erro ao deletar estoque.",
                value=sku,
            )
        else:
            logger.debug(f"Estoque deletado seller_id={seller_id}, sku={sku}")

    async def list(self, paginator: Paginator, filters: dict) -> list[Estoque]:
        """
        Lista todos os estoques, aplicando filtros e paginação.
        """
        logger.debug(f"Listando estoques com filtros={filters} e paginação limit={paginator.limit}, offset={paginator.offset}")
        resultados_filtrados = await self.repository.find(
            filters,
            limit=paginator.limit,
            offset=paginator.offset
        )
        return resultados_filtrados

    def _validate_positive_estoque(self, estoque):
        """
        Valida se a 'quantidade' do estoque é positiva.
        """
        if estoque.quantidade <= 0:
            logger.warning(f"Quantidade inválida para estoque: {estoque.quantidade}")
            self._raise_bad_request("quantidade deve ser maior que zero.", "quantidade", estoque.quantidade)

    async def _validate_non_existent_estoque(self, seller_id: str, sku: str):
        """
        Verifica se já existe um estoque cadastrado para o seller_id e sku informados.
        """
        estoque_found = await self.repository.find_by_seller_id_and_sku(seller_id, sku)
        if estoque_found is not None:
            logger.warning(f"Estoque já cadastrado para seller_id={seller_id}, sku={sku}")
            self._raise_bad_request("Estoque para produto já cadastrado.", "sku")

    @staticmethod
    def _raise_not_found(seller_id: str, sku: str, condition: bool = True):
        """
        Lança exceção de NotFoundException com detalhes do erro.
        """
        if condition:
            logger.error(f"Estoque não encontrado para seller_id={seller_id}, sku={sku}")
            raise EstoqueNotFoundException(seller_id=seller_id, sku=sku)

    def _raise_bad_request(self, message: str, field: str = None, value=None):
        """
        Lança exceção de BadRequestException com detalhes do erro.
        """
        logger.error(f"BadRequestException: {message}, field={field}, value={value}")
        raise EstoqueBadRequestException(message=message, field=field, value=value)