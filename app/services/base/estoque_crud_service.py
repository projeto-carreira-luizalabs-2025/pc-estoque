from typing import Any, Generic, TypeVar
import logging  # Importação do módulo de logging para registrar informações e erros

# Importação de classes específicas do projeto
from app.api.common.schemas import Paginator  # Classe de paginação para controlar os resultados
from app.models.estoque_model import Estoque  # Modelo Pydantic de Estoque
from app.repositories.base.estoque_memory_repository import AsyncMemoryRepository  # Repositório de memória assíncrono

# Definição de tipos genéricos
T = TypeVar("T", bound=Estoque)  # T representa o modelo de Estoque
ID = TypeVar("ID", bound=str)  # ID é do tipo string (ou outro tipo conforme necessário)

# Serviço CRUD para manipulação do estoque
class EstoqueCrudService(Generic[T, ID]):
    def __init__(self, repository: AsyncMemoryRepository[T, ID], context: Any = None):
        self.repository = repository  # Repositório de memória para operações de CRUD
        self._context = context  # Contexto opcional (útil para informações extras como vendedor logado)

    @property
    def context(self):
        return self._context

    @property
    def author(self):
        # Retorna o vendedor associado ao contexto, se existir
        if self.context and hasattr(self.context, "seller"):
            return self.context.seller

    def _validate_quantidade(self, quantidade: Any) -> None:
        """Valida se a quantidade é um inteiro não negativo"""
        if not isinstance(quantidade, int) or quantidade < 0:
            raise ValueError("Quantidade informada deve ser um número inteiro positivo ou zero")

    async def create(self, entity: Estoque) -> Estoque:
        """Cria um novo registro de estoque"""
        self._validate_quantidade(entity.quantidade)  # Valida a quantidade
        created_entity = await self.repository.create(entity)  # Cria o estoque no repositório
        logging.info(f"Registro criado com sucesso: {created_entity}")  # Log de sucesso
        return created_entity

    async def find_by_id(self, entity_id: ID) -> Estoque | None:
        """Busca um registro de estoque pelo ID"""
        entity = await self.repository.find_by_id(entity_id)
        if not entity:
            logging.warning(f"Registro com ID {entity_id} não encontrado")
        return entity

    async def find(self, paginator: Paginator, filters: dict) -> list[T]:
        """Busca registros com filtros e paginação"""
        logging.info(f"Buscando registros com filtros: {filters}, "
                     f"limit={paginator.limit}, offset={paginator.offset}, "
                     f"ordenado por: {paginator.get_sort_order()}")
        
        # Chama o repositório para buscar com filtros e ordenação
        return await self.repository.find(
            filters=filters,
            limit=paginator.limit,
            offset=paginator.offset,
            sort=paginator.get_sort_order()
        )

    async def update(self, entity_id: ID, entity: Estoque) -> Estoque:
        """Atualiza um registro de estoque ou cria um novo se não existir"""
        self._validate_quantidade(entity.quantidade)  # Valida a quantidade antes de atualizar

        existing_entity = await self.repository.find_by_id(entity_id)
        if existing_entity:
            # Atualiza o estoque existente
            updated_entity = await self.repository.update(entity_id, entity)
            logging.info(f"Registro com ID {entity_id} atualizado com sucesso: {updated_entity}")
        else:
            # Se não existir, cria um novo estoque
            updated_entity = await self.repository.create(entity)
            logging.info(f"Registro criado com sucesso (ID inexistente): {updated_entity}")

        return updated_entity

    async def delete_by_id(self, entity_id: ID) -> None:
        """Deleta um registro de estoque pelo ID"""
        entity = await self.repository.find_by_id(entity_id)
        if not entity:
            raise ValueError(f"Registro com ID {entity_id} não encontrado")  # Levanta erro se não existir

        await self.repository.delete_by_id(entity_id)  # Deleta o estoque
        logging.info(f"Registro com ID {entity_id} deletado com sucesso")

