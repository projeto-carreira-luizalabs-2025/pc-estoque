from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import json

# Criando o router com prefixo /estoque
estoque_routes = APIRouter(prefix="/api/estoque", tags=["Estoque"])

# Modelo para os itens de estoque
class ItemEstoque(BaseModel):
     
    """
    Representa um item no estoque.
    
    Atributos:
    - seller_id: Identificador do vendedor.
    - sku: Identificador do produto.
    - quantidade: Quantidade disponível em estoque.
    """
     
    seller_id: str
    sku: str
    quantidade: int


# Caminho para o arquivo JSON
DATA_PATH = "app/data/estoque.json"

# Função auxiliar para carregar o estoque
def carregar_estoque():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Função auxiliar para salvar o estoque
def salvar_estoque(estoque):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(estoque, f, indent=4)

# Rota para listar todos os itens
@estoque_routes.get("/", response_model=List[ItemEstoque])
async def listar_estoque():
    """
    Lista todos os itens do estoque.

    Retorna:
        Lista de objetos ItemEstoque.

        Atributos de ItemEstoque:
        - seller_id: Identificador do vendedor.
        - sku: Identificador do produto.
        - quantidade: Quantidade disponível em estoque.

        Exemplo:
        {
        "seller_id": "3",
        "sku": "Monitor 24''",
        "quantidade": 5, 
        }
    """
    return carregar_estoque()

# Rota para adicionar um novo item
@estoque_routes.post("/", response_model=ItemEstoque)
async def adicionar_item(item: ItemEstoque):
    """
    Adiciona um novo item ao estoque.

    Parâmetros:
        item: Objeto ItemEstoque a ser adicionado.

        Atributos de ItemEstoque:
        - seller_id: Identificador do vendedor.
        - sku: Identificador do produto.
        - quantidade: Quantidade disponível em estoque.

    Retorna:
        O item adicionado.
    """
    estoque = carregar_estoque()
    estoque.append(item.dict())
    salvar_estoque(estoque)
    return item

# Rota para buscar um item pelo seller_id e sku
@estoque_routes.get("/{seller_id}/{sku}", response_model=ItemEstoque)
async def buscar_item(seller_id: str, sku: str):
    """
    Busca um item no estoque com base no seller_id e sku.

    Parâmetros:
        seller_id: Identificador do vendedor.
        sku: Identificador do produto.

    Retorna:
        O item correspondente, se encontrado.

    Erros:
        404 - Item não encontrado.
    """
    estoque = carregar_estoque()
    for item in estoque:
        if item["seller_id"] == seller_id and item["sku"] == sku:
            return item
    raise HTTPException(status_code=404, detail="Item não encontrado")

# Rota para consultar estoque por seller ou sku com paginação
@estoque_routes.get("/buscar/", response_model=List[ItemEstoque])
async def buscar_estoque(
    seller_id: Optional[str] = None,
    sku: Optional[str] = None,
    page: int = Query(1, gt=0),
    page_size: int = Query(10, gt=0, le=100)
):
    """
    Busca itens no estoque filtrando por seller_id e/ou sku, com suporte à paginação.

    Parâmetros:
        seller_id: (opcional) ID do vendedor para filtro.
        sku: (opcional) Código do produto para filtro.
        page: Número da página (padrão: 1).
        page_size: Tamanho da página (padrão: 10, máximo: 100).

    Retorna:
        Lista paginada de itens filtrados.
    """

    estoque = carregar_estoque()

    resultados = [
        item for item in estoque
        if (seller_id is None or item["seller_id"] == seller_id)
        and (sku is None or item["sku"] == sku)
    ]

    start = (page - 1) * page_size
    end = start + page_size
    paginados = resultados[start:end]

    return paginados

# Rota para atualizar um item pelo seller_id e sku
@estoque_routes.put("/{seller_id}/{sku}", response_model=ItemEstoque)
async def atualizar_item(seller_id: str, sku: str, item_atualizado: ItemEstoque):
    """
    Atualiza os dados de um item existente com base em seller_id e sku.

    Parâmetros:
        seller_id: ID do vendedor.
        sku: Código do produto.
        item_atualizado: Novo objeto ItemEstoque com os dados atualizados.

    Retorna:
        O item atualizado.

    Erros:
        404 - Item não encontrado.
    """
    estoque = carregar_estoque()
    for index, item in enumerate(estoque):
        if item["seller_id"] == seller_id and item["sku"] == sku:
            estoque[index] = item_atualizado.dict()
            salvar_estoque(estoque)
            return item_atualizado
    raise HTTPException(status_code=404, detail="Item não encontrado")

# Rota para deletar um item pelo seller_id e sku
@estoque_routes.delete("/{seller_id}/{sku}")
async def deletar_item(seller_id: str, sku: str):
    """
    Deleta um item do estoque com base em seller_id e sku.

    Parâmetros:
        seller_id: ID do vendedor.
        sku: Código do produto.

    Erros:
        404 - Item não encontrado.
    """
    estoque = carregar_estoque()
    for index, item in enumerate(estoque):
        if item["seller_id"] == seller_id and item["sku"] == sku:
            del estoque[index]
            salvar_estoque(estoque)
            return
    raise HTTPException(status_code=404, detail="Item não encontrado")