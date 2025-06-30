# 📦 PC-Estoque

## 📄 Descrição

O PC-Estoque é um sistema de gerenciamento de estoque desenvolvido para oferecer uma solução simples, prática e eficiente no controle de produtos disponíveis em marketplaces. A aplicação permite realizar o cadastro de produtos, controlar entradas e saídas de estoque, atualizar quantidades disponíveis e visualizar informações em tempo real — garantindo maior organização, segurança e agilidade nas operações comerciais.

## 👥 Equipe de Desenvolvimento

- Elbia Simone Buglio
- Laura Gabriely
- Victor Teixeira

## 💻 Tecnologias Utilizadas

Este projeto foi construído utilizando as seguintes tecnologias principais:

- **Python 3.12**
- **FastAPI**: Framework web para a construção de APIs.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **PostgreSQL**: Banco de dados relacional.
- **Alembic**: Ferramenta para gerenciamento de migrações de banco de dados.
- **Docker & Docker Compose**: Para containerização da aplicação e seus serviços.
- **Pytest**: Para a execução dos testes automatizados.
- **Keycloak**: Para gerenciamento de identidade e acesso.

## 🚀 Como Rodar o Projeto

Existem duas maneiras principais de executar este projeto: **localmente** (ideal para desenvolvimento e depuração) ou via **Docker** (simula um ambiente de produção).

### 1. Configuração e Execução Local

Siga os passos abaixo para configurar o ambiente de desenvolvimento na sua máquina.

#### **Pré-requisitos**

- Python 3.12
- Um servidor de banco de dados PostgreSQL em execução.

#### **Clonando o Repositório**

```bash
git clone https://github.com/projeto-carreira-luizalabs-2025/pc-estoque.git
cd pc-estoque
```

#### **Configuração do Ambiente (Linux 🐧)**

1.  **Crie o ambiente virtual:**
    ```bash
    make build-venv
    ```
2.  **Ative o ambiente virtual:**
    ```bash
    source ./venv/bin/activate
    ```
3.  **Instale as dependências:**
    ```bash
    make requirements-dev
    ```

#### **Configuração do Ambiente (Windows 🪟)**

1.  **Crie o ambiente virtual:**
    ```bash
    python -m venv venv
    ```
2.  **Ative o ambiente virtual:**
    ```bash
    .\venv\Scripts\activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements/develop.txt
    ```

#### **Configurando Variáveis de Ambiente e Banco de Dados Para o Ambiente de Desenvolvimento**

1.  **Copie o arquivo de ambiente:** Este arquivo contém as configurações necessárias para a aplicação, como a URL do banco de dados.

    ```bash
    # No Linux
    make load-dev-env

    # No Windows
    copy devtools\dotenv.dev .env
    ```

2.  **Ajuste o arquivo `.env`:** Abra o arquivo `.env` recém-criado e altere a variável `APP_DB_URL` para apontar para o seu banco de dados PostgreSQL local. O formato é: `postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DATABASE_NAME`.

3.  **Aplique as migrações do banco de dados:** Para criar as tabelas necessárias, execute o Alembic.

    ```bash
    # No Linux
    make migration

    # No Windows
    alembic upgrade head
    ```

#### **Configurando Variáveis de Ambiente e Banco de Dados Para o Ambiente de Teste**

1.  **Copie o arquivo de ambiente:** Este arquivo contém as configurações necessárias para a aplicação, como a URL do banco de dados.

    ```bash
    # No Linux
    make load-test-env

    # No Windows
    copy devtools\dotenv.test .env
    ```

2.  **Ajuste o arquivo `.env`:** Abra o arquivo `.env` recém-criado e altere a variável `APP_DB_URL` para apontar para o seu banco de dados PostgreSQL local. O formato é: `postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DATABASE_NAME`.

3.  **Aplique as migrações do banco de dados:** Para criar as tabelas necessárias, execute o Alembic.

    ```bash
    # No Linux
    make migration

    # No Windows
    alembic upgrade head
    ```

#### **Executando a Aplicação**

Com o ambiente virtual ativado, inicie o servidor da API:

```bash
make run-dev
```

Ou, manualmente:

```bash
uvicorn app.api_main:app --reload
```

### 2. Comfiguração e Execução com Docker

obs: O docker-compose esta configurado para subir a Api, o banco de dados e o Keycloak.

O Docker simplifica todo o processo, gerindo a aplicação, a base de dados e o Keycloak em contentores isolados. Siga os passos abaixo:

#### **Pré-requisitos**

- Docker
- Docker Compose

#### **Passo 1: Preparar Variáveis de Ambiente**

Antes de iniciar, é necessário criar um ficheiro de configuração `.env`. Pode copiar o ficheiro de exemplo fornecido.

- **No Linux/macOS:**
  ```bash
  make load-dev-env
  ```
- **No Windows:**
  ```bash
  copy devtools\dotenv.dev .env
  ```
  _(Este ficheiro já vem pré-configurado para o ambiente Docker, pelo que não são necessários ajustes.)_

#### **Passo 2: Iniciar a Aplicação (App + Banco de Dados + Keycloak)**

Este comando irá iniciar os contêineres da aplicação e do banco de dados PostgreSQL e o Keycloak, alem de realizar a migração do banco de dados e carregar o estoque inicial.

```bash
  # No Linux
  make docker-up

  # No Windows
  docker-compose -f docker-compose-keycloak.yml -f docker-compose.yml up -d
  docker-compose exec app alembic upgrade head
  docker-compose exec app python devtools/scripts/carregar_estoque_inicial.py

```

Aguarde alguns instantes para que os serviços estejam operacionais.

#### **Passo 4 (Opcional): Iniciar Serviços Adicionais**

Se você precisar dos outros serviços, como o **SonarQube**, inicie-os com seus respectivos arquivos do Compose.

- **Para o SonarQube:**
  ```bash
  docker-compose -f docker-compose-sonar.yml up -d
  ```

#### **Comandos Úteis do Docker**

- **Para parar a aplicação principal (app e db):**
  ```bash
  make  down
  ```
- **Para parar um serviço adicional (ex: sonar):**
  ```bash
  docker-compose -f docker-compose-sonar.yml down
  ```

## 🧪 Testes e Qualidade de Código

O projeto está configurado com um conjunto de ferramentas para garantir a qualidade e a consistência do código.

### **Configurando Variáveis de Ambiente e Banco de Dados Para o Ambiente de Teste**

1.  **Copie o arquivo de ambiente:** Este arquivo contém as configurações necessárias para a aplicação, como a URL do banco de dados.

    ```bash
    # No Linux
    make load-test-env

    # No Windows
    copy devtools\dotenv.test .env
    ```

2.  **Ajuste o arquivo `.env`:** Abra o arquivo `.env` recém-criado e altere a variável `APP_DB_URL` para apontar para o seu banco de dados PostgreSQL local. O formato é: `postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DATABASE_NAME`.

3.  **Aplique as migrações do banco de dados:** Para criar as tabelas necessárias, execute o Alembic.

    ```bash
    # No Linux
    make migration

    # No Windows
    alembic upgrade head
    ```

### **Executando os Testes**

Para rodar a suíte de testes unitários e de integração, utilize o Pytest:

```bash
# No Linux
make test

# No Windows
pytest
```

Para gerar um relatório de cobertura de testes, execute:

```bash
# No Linux
make coverage

# No Windows
pytest --cov=app --cov-report=html
```

O relatório será gerado na pasta `htmlcov/`. Você pode abrir o arquivo `index.html` em seu navegador para visualizar os detalhes.

### **Análise com SonarQube**

O projeto está configurado para análise com o SonarQube.

1.  **Inicie o SonarQube:**

    ```bash
    docker-compose -f docker-compose-sonar.yml up -d
    ```

2.  **Execute o Scanner:** Após rodar os testes e gerar o `coverage.xml`, execute o scanner do Sonar para enviar os resultados para o servidor. Você precisará de um token de autenticação.
    ```bash
    docker run --rm \
     -e SONAR_HOST_URL=http://localhost:9000 \
     -e SONAR_TOKEN="SEU_TOKEN_AQUI" \
     -v "$(pwd)":/usr/src \
     sonarsource/sonar-scanner-cli
    ```

## 📖 Documentação da API

Após iniciar a aplicação (localmente ou com Docker), você pode acessar a documentação interativa da API nos seguintes endereços:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 📫 Contribuições

O projeto está aberto a contribuições. O fluxo para contribuição é o seguinte:

1.  Realize um **fork** do repositório.
2.  Crie uma **branch** descritiva para a sua feature ou correção.
3.  Submeta um **Pull Request**.
4.  Aguarde o **Code Review** pela equipe de desenvolvimento.
5.  Após a aprovação, sua alteração será integrada ao código principal.
