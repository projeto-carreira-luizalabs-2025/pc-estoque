from pydantic import Field, PostgresDsn, HttpUrl
import dotenv
import os

from .base import BaseSettings

ENV = os.getenv("ENV", "production")
is_dev = ENV == "dev"

dotenv.load_dotenv(override=is_dev)

class AppSettings(BaseSettings):
    version: str = Field(default="0.5.0", title="Versão da aplicação")

    app_name: str = Field(default="PC Estoque", title="Nome da aplicação")

    memory_min: int = Field(default=64, title="Limite mínimo de memória disponível em MB")
    disk_usage_max: int = Field(default=80, title="Limite máximo de 80% de uso de disco")

    app_db_url: PostgresDsn = Field(..., title="URI para o banco Postgresql")

    app_openid_wellknown: HttpUrl = Field(..., title="URL well-known do Keycloak")

settings = AppSettings()



