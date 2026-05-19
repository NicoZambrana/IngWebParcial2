from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class Colaborador(BaseModel):
    email: EmailStr
    nombre: str
    habilidades: List[str]
    segmento_asignado : int

class Tarea(BaseModel):
    responsable: EmailStr
    descripcion: str = Field(..., max_length=50)
    habilidades: List[str]
    segmentos: int
    colaboradores: List[Colaborador]



