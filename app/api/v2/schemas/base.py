from datetime import datetime
from typing import TypeAlias
from uuid import UUID as UuidType

from pydantic import BaseModel, Field

ModelSchema: TypeAlias = BaseModel


# Pydantic Mixins
class UuidMixinSchema(BaseModel):
    id: UuidType | None = Field(None, description="Identificador do objeto")


class TimestampMixinSchema(BaseModel):
    created_at: datetime | None = Field(None, description="Data e hora da criação")
    updated_at: datetime | None = Field(None, description="Data e hora da atualização")
