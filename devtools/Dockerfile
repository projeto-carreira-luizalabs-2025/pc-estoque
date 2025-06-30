# Etapa de build: cria o ambiente virtual e instala dependências
FROM python:3.12-slim AS build

WORKDIR /app

# Copia apenas os arquivos necessários
COPY requirements.txt .
COPY requirements ./requirements/

# Cria o virtualenv e instala os pacotes diretamente nele
RUN python -m venv venv && \
    ./venv/bin/pip install --upgrade pip && \
    ./venv/bin/pip install --no-cache-dir -r requirements.txt && \
    ./venv/bin/pip install --no-cache-dir -r requirements/develop.txt

# Imagem final
FROM python:3.12-slim

WORKDIR /pc-estoque

# Copia o .env (variáveis de ambiente)
COPY devtools/dotenv.dev /pc-estoque/.env

# Copia o ambiente virtual do estágio anterior
COPY --from=build /app/venv /app/venv

# Copia o código da aplicação
COPY . .

# Compila os arquivos .py
RUN python -m compileall app

# Define o PATH para usar o venv copiado
ENV PATH="/app/venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.api_main:app", "--host", "0.0.0.0", "--port", "8000"]