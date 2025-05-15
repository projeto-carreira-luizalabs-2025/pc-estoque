from pathlib import Path
import json

# Caminho para o arquivo JSON onde os dados do estoque ficarão salvos
DATA_PATH = Path("app/data/estoque.json")

# Verifica se o arquivo existe. Se não, cria um com uma lista vazia
if not DATA_PATH.exists():
    print("Arquivo estoque.json não encontrado, criando um novo...")
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4)

# Define os dados iniciais de estoque (você pode personalizar aqui)
estoque_inicial = [
    {
        "seller_id": "1",
        "sku": "Mouse Gamer",
        "quantidade": 15,
       
    },
    {
        "seller_id": "2",
        "sku": "Teclado Mecânico",
        "quantidade": 10,
        
    },
    {
        "seller_id": "3",
        "sku": "Monitor 24''",
        "quantidade": 5, 
    }
]

# Salva os dados no arquivo JSON
with open(DATA_PATH, "w", encoding="utf-8") as f:
    json.dump(estoque_inicial, f, indent=4, ensure_ascii=False)

print("Estoque inicial carregado com sucesso em", DATA_PATH)

