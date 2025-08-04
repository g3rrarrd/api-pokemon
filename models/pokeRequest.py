from pydantic import BaseModel, Field
from typing import Optional, List

class PokeRequest(BaseModel):
    id: Optional[int] = Field(
        default=None,
        ge=1,
        description="ID de la repeticion"
        )
    
    pokemon_type: Optional[str] = Field(
        default=None,
        description="Tipo de Pokemon",
        pattern="^[a-zA-Z0-9_]+$"
    )

    url: Optional[str] = Field(
        default=None,
        description="URL del Pokemon",
        pattern="^https?://(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(?:/[a-zA-Z0-9_~%\-\.&=?]*)*$",
        max_length=255
    )

    status: Optional[str] = Field(  
        default=None,
        description="Estado de la repeticion",
        pattern="^(En cola|En proceso|Finalizado|Error)$"
    )

