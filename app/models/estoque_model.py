from pydantic import BaseModel, Field, field_validator
from typing import Optional
import uuid


class Estoque(BaseModel):
    # Gera um ID único automaticamente
    identity: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    seller_id: str
    sku: str
    quantidade: int = Field(..., ge=0)  # ge=0 já garante que não seja negativo

    # Validação adicional para quantidade (opcional, pois o Field já faz isso)
    @field_validator("quantidade")
    @classmethod
    def validate_quantidade(cls, v):
        if v < 0:
            raise ValueError("A quantidade não pode ser negativa.")
        return v

