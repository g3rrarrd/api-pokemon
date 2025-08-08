from pydantic import BaseModel, Field
from typing import Optional, List

class PokeRequest(BaseModel):
    id: Optional[int] = Field(
        default=None,
        ge=1,
        description="ID de la peticion"
    )

    pokemon_type: Optional[str] = Field(
        default=None,
        description="Tipo de pokemon",
        pattern="^[a-zA-Z0-9_]+$"
    )

    url: Optional[str] = Field(
        default=None,
        description="URL de la peticion",
        pattern=r"^$|^https?://[^\s]+$",
        max_length=255
    )


    status: Optional[str] = Field(
        default=None,
        description="Estado de la peticion",
        pattern="^(En Cola|Finalizado|Error|En proceso)$"
    )

    sample_size: Optional[int] = Field(
        None,
        gt=0
    )