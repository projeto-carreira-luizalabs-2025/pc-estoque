# Primeira etapa: instalar os pacotes do Python
# Montar a estrutura de arquivos da aplicação
FROM python:3.12-slim as construtor

SHELL ["/bin/bash", "-c"]

WORKDIR /app

COPY requirements.txt .
COPY requirements ./requirements/


RUN pip install --upgrade pip && pip install -r ./requirements.txt
RUN pip install --upgrade pip && pip install -r ./requirements/develop.txt


# Instalar meus pacotes
RUN pip install --upgrade pip && \
    python -m venv venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt && \
    /app/venv/bin/pip install --no-cache-dir -r requirements/develop.txt


# Etapa final (imagem leve)
FROM python:3.12-slim

WORKDIR /pc-estoque

COPY devtools/dotenv.dev /pc-estoque/.env


# Copia o ambiente virtual
COPY --from=construtor /app/venv /app/venv

# Copia a aplicação inteira
COPY . .

# Compilar os arquivos .py
RUN python -m compileall app

# Variável de ambiente para usar o venv
ENV PATH="/app/venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.api_main:app", "--host", "0.0.0.0", "--port", "8000"]
# Se quiser versionar:r
    #docker build -f devtools/Dockerfile -t pc-estoque:0.0.1 .
    #docker run -p 8000:8000 -e ENV=dev pc-estoque:0.0.1

