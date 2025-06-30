APP_DIR?=app
ROOT_TESTS_DIR?=tests
SCRIPTS_DIR?=scripts
ENV?="$$(dotenv get ENV)"
MAKE_ARGS?=--no-print-directory
API_PATH := ${APP_DIR}/
API_MODULE_MAIN := ${APP_DIR}.api_main
HOST?=0.0.0.0
PORT?=8000
INIT?=uvicorn ${API_MODULE_MAIN}:app --host $(HOST) --port $(PORT)

clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "*.log" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -f .coverage.NB-SBDEV*
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f *.log
	@rm -f .env.bkp*

build-venv:
	python3.12 -m venv venv

requirements-dev:
	pip install --upgrade pip
	@pip install -r requirements/develop.txt


lint:
	isort ${APP_DIR} ${ROOT_TESTS_DIR}
	bandit -c pyproject.toml -r -f custom ${APP_DIR} ${ROOT_TESTS_DIR}
	black ${APP_DIR} ${ROOT_TESTS_DIR}
	flake8 --max-line-length=120 ${APP_DIR} ${ROOT_TESTS_DIR}

check-lint:
	isort -c ${APP_DIR} ${ROOT_TESTS_DIR}
	bandit -c pyproject.toml -r -f custom ${APP_DIR} ${ROOT_TESTS_DIR}
	black --check ${APP_DIR} ${ROOT_TESTS_DIR}
	flake8 --max-line-length=120 ${APP_DIR} ${ROOT_TESTS_DIR}
	mypy ${APP_DIR} ${SCRIPTS_DIR} ${MIGRATIONS_DIR} ${ROOT_TESTS_DIR}

safety:
	@pip-audit -r requirements/base.txt

dead-fixtures:
	@ENV=$(ENV) pytest --dead-fixtures


.PHONY: build
build: lint-check test


pop-env:
	@./devtools/scripts/pop-env

load-env:
	@./devtools/scripts/push-env "devtools/dotenv.$(env)"

load-dev-env:
	@env=dev make $(MAKE_ARGS) load-env

load-test-env:
	@env=test make $(MAKE_ARGS) load-env

.PHONY: run
run:
	$(INIT)

run-dev:
	@ENV=$(ENV) $(INIT) --reload

test:
	PYTHONPATH=. pytest


# Realizar a migração do banco de dados
migration:
	alembic upgrade head

# Testar fazendo a cobertura do código
coverage:
	pytest --cov=${APP_DIR} --cov-report=term-missing --cov-report=xml ${ROOT_TESTS_DIR} --cov-fail-under=80 --durations=5

# Subir o docker para os testes com o Keycloak
docker-tests-up:
	docker-compose up -d --build
	docker-compose -f docker-compose-keycloak.yml up -d --build
	docker-compose exec app alembic upgrade head
	docker-compose exec app python devtools/scripts/carregar_estoque_inicial.py

# Descer e remover o docker dos testes com o Keycloak
docker-tests-down:
	docker-compose down -d
	docker-compose -f docker-compose-keycloak.yml down -d

# Subir a aplicação com o Keycloak
docker-up:
	docker-compose up -d --build
	docker-compose -f docker-compose-keycloak.yml up -d --build
	docker-compose exec app alembic upgrade head
	docker-compose exec app python devtools/scripts/carregar_estoque_inicial.py


# Descer e remover a aplicação com o Keycloak
docker-down:
	docker-compose down -d
	docker-compose -f docker-compose-keycloak.yml down -d