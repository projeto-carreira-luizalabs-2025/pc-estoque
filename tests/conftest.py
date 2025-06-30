import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from datetime import datetime

import tempfile
import os
from uuid import uuid4

# 🔸 Banco fake (simulação)
fake_db = {}

# 🔸 Variável global/singleton
GLOBAL_CONFIG = {"user": "admin"}

# 🔸 Cache em memória
cache = {}

# 🔸 Fixture que faz setup e teardown antes/depois de cada teste
@pytest.fixture(autouse=True)
def limpar_ambiente_de_teste(tmp_path):
    print("\n[Setup] Preparando ambiente de teste...")

    # Resetar banco fake
    fake_db.clear()

    # Resetar variável global
    GLOBAL_CONFIG["user"] = "admin"

    # Limpar cache
    cache.clear()

    # Criar diretório temporário (tmp_path já faz isso)
    temp_dir = tmp_path

    # Criar mock e resetar se necessário
    mock_service = MagicMock()

    yield {
        "fake_db": fake_db,
        "global_config": GLOBAL_CONFIG,
        "cache": cache,
        "temp_dir": temp_dir,
        "mock_service": mock_service
    }

    print("[Teardown] Limpando ambiente de teste...")

    # Apagar arquivos temporários, se criados
    for file in os.listdir(temp_dir):
        os.remove(temp_dir / file)

    # Resetar mocks
    mock_service.reset_mock()

@pytest.fixture(autouse=True)
def limpa_antes_e_depois():
    print("\nSetup antes de cada teste")
    yield
    print("Teardown depois de cada teste")

# 🔸 Fixture para UUID falso
@pytest.fixture
def fake_uuid():
    """
    Fixture que retorna um UUID4 falso para uso nos testes.
    """
    return uuid4()

# 🔸 Fixture para data e hora fixa
@pytest.fixture
def fake_datetime():
    """
    Fixture que retorna uma data e hora fixa para uso nos testes.
    """
    return datetime(2024, 6, 22, 12, 0, 0)

# 🔸 Fixture para mock das configurações da aplicação
@pytest.fixture
def mock_settings():
    """
    Fixture que retorna um mock para as configurações da aplicação.
    """
    return MagicMock()

# 🔸 Fixture para mock do cliente SQL
@pytest.fixture
def mock_sql_client():
    """
    Fixture que retorna um mock para o cliente SQL.
    """
    return MagicMock()

# 🔸 Fixture para mock do repositório de estoque
@pytest.fixture
def mock_estoque_repository():
    """
    Fixture que retorna um mock para o repositório de estoque.
    """
    return MagicMock()

# 🔸 Fixture para mock do serviço de health check
@pytest.fixture
def mock_health_check_service():
    """
    Fixture que retorna um mock para o serviço de health check.
    """
    return MagicMock()

# 🔸 Fixture para mock do serviço de estoque
@pytest.fixture
def mock_estoque_service():
    """
    Fixture que retorna um mock para o serviço de estoque.
    """
    return MagicMock()