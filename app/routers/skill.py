from fastapi import APIRouter, HTTPException
from typing import List
from ..models import Colaborador
from ..database import db


router = APIRouter()

@router.get("/collaborators/{email}/skills", response_model=List[str])
async def get_all_skills(email: str):
    """
    Obtiene todas las habilidades de un colaborador.

    Esta función busca un colaborador en la base de datos utilizando el email proporcionado.
    Si el colaborador se encuentra, retorna una lista de sus habilidades.
    Si el colaborador no se encuentra, lanza una excepción HTTP 404.

    Args:
        email (str): El email del colaborador.

    Returns:
        List[str]: Una lista de habilidades del colaborador.
    """
    collaborator = await db["collabs"].find_one({"email": email})
    if not collaborator:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    return collaborator.get("habilidades", [])

@router.post("/collaborators/{email}/skills", response_model=List[str])
async def add_skill(email: str, skill: str):
    """
    Añade una habilidad a un colaborador.

    Esta función busca un colaborador en la base de datos utilizando el email proporcionado.
    Si el colaborador se encuentra, añade la habilidad proporcionada a su lista de habilidades.
    Si la habilidad ya existe, lanza una excepción HTTP 400.
    Si el colaborador no se encuentra, lanza una excepción HTTP 404.

    Args:
        email (str): El email del colaborador.
        skill (str): La habilidad a añadir.

    Returns:
        List[str]: La lista actualizada de habilidades del colaborador.
    """
    collaborator = await db["collabs"].find_one({"email": email})
    if not collaborator:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    if skill in collaborator.get("habilidades", []):
        raise HTTPException(status_code=400, detail="La habilidad ya existe")
    await db["collabs"].update_one({"email": email}, {"$push": {"habilidades": skill}})
    return collaborator["habilidades"] + [skill]

@router.delete("/collaborators/{email}/skills/{skill}")
async def delete_skill(email: str, skill: str):
    """
    Elimina una habilidad de un colaborador.

    Esta función busca un colaborador en la base de datos utilizando el email proporcionado.
    Si el colaborador se encuentra, elimina la habilidad proporcionada de su lista de habilidades.
    Si la habilidad no existe, lanza una excepción HTTP 400.
    Si el colaborador no se encuentra, lanza una excepción HTTP 404.

    Args:
        email (str): El email del colaborador.
        skill (str): La habilidad a eliminar.

    Returns:
        List[str]: La lista actualizada de habilidades del colaborador.
    """
    collaborator = await db["collabs"].find_one({"email": email})
    if not collaborator:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    if skill not in collaborator.get("habilidades", []):
        raise HTTPException(status_code=404, detail="Habilidad no encontrada")
    await db["collabs"].update_one({"email": email}, {"$pull": {"habilidades": skill}})
    return {"detail": "Habilidad eliminada con éxito"}
