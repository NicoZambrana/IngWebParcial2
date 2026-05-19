from fastapi import APIRouter, HTTPException
from typing import List
from ..database import db
from ..models import Colaborador

router = APIRouter()

@router.get("/collaborators/", response_model=List[Colaborador])
async def get_all_collaborators():
    """
    Obtiene todos los colaboradores.

    Esta función obtiene una lista de todos los colaboradores almacenados en la base de datos.
    Retorna una lista de objetos de tipo Colaborador.

    Returns:
        List[Colaborador]: Una lista de colaboradores.
    """
    collaborators = await db["collabs"].find().to_list(1000)
    return collaborators

@router.get("/collaborators/{email}", response_model=Colaborador)
async def get_collaborator(email: str):
    """
    Obtiene un colaborador específico por su email.

    Esta función busca un colaborador en la base de datos utilizando el email proporcionado.
    Si el colaborador no se encuentra, lanza una excepción HTTP 404.

    Args:
        email (str): El email del colaborador a buscar.

    Returns:
        Colaborador: El objeto Colaborador encontrado.
    """
    collaborator = await db["collabs"].find_one({"email": email})
    if not collaborator:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    return collaborator

@router.post("/collaborators/", response_model=Colaborador)
async def create_collaborator(collaborator: Colaborador):
    """
    Crea un nuevo colaborador.

    Esta función recibe un objeto Colaborador y lo inserta en la base de datos.
    Si el colaborador ya existe, lanza una excepción HTTP 400.

    Args:
        collaborator (Colaborador): El objeto Colaborador a crear.

    Returns:
        Colaborador: El objeto Colaborador creado.
    """
    if await db["collabs"].find_one({"email": collaborator.email}):
        raise HTTPException(status_code=400, detail="El colaborador ya existe")
    await db["collabs"].insert_one(collaborator.model_dump())
    return collaborator

@router.delete("/collaborators/{email}")
async def delete_collaborator(email: str):
    """
    Elimina un colaborador existente.

    Esta función elimina un colaborador de la base de datos utilizando el email proporcionado.
    Si el colaborador no se encuentra, lanza una excepción HTTP 404.

    Args:
        email (str): El email del colaborador a eliminar.

    Returns:
        dict: Un mensaje de éxito si el colaborador fue eliminado.
    """
    result = await db["collabs"].delete_one({"email": email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")
    return {"detail": "Colaborador eliminado con éxito"}

@router.get("/collaborators/responsable/{responsable_email}", response_model=List[str])
async def get_collaborators_by_responsable(responsable_email: str):
    """
    Obtiene los colaboradores de un determinado usuario.

    Esta función busca los colaboradores que participan en alguna de las tareas de las que el usuario es responsable.
    Retorna una lista de emails de colaboradores.

    Args:
        responsable_email (str): El email del usuario responsable.

    Returns:
        List[str]: Una lista de emails de colaboradores.
    """
    tasks = await db["tasks"].find({"responsable": responsable_email}).to_list(1000)
    collaborator_emails = set()
    for task in tasks:
        for collaborator in task["colaboradores"]:
            collaborator_emails.add(collaborator["email"])
    return list(collaborator_emails)