

from fastapi import APIRouter, HTTPException
from typing import List
from ..database import db
from ..models import Tarea
from bson import ObjectId

router = APIRouter()

@router.get("/tasks/", response_model=List[Tarea])
async def get_all_tasks():
    """
    Obtiene todas las tareas.

    Esta función obtiene una lista de todas las tareas almacenadas en la base de datos.
    Retorna una lista de objetos de tipo Tarea.
    """
    tasks = await db["tasks"].find().to_list(1000)
    return tasks

@router.get("/tasks/{task_id}", response_model=Tarea)
async def get_task(task_id: str):
    """
    Obtiene una tarea específica por su ID.

    Esta función busca una tarea en la base de datos utilizando el ID proporcionado.
    Si la tarea no se encuentra, lanza una excepción HTTP 404.
    
    Args:
        task_id (str): El ID de la tarea a buscar.

    Returns:
        Tarea: El objeto Tarea encontrado.
    ID DE PRUEBA: 67377d455562581293c248e9
    """
    task = await db["tasks"].find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task

@router.post("/tasks/", response_model=Tarea)
async def create_task(task: Tarea):
    """
    Crea una nueva tarea.

    Esta función recibe un objeto Tarea y lo inserta en la base de datos.
    Retorna el objeto Tarea creado.
    
    Args:
        task (Tarea): El objeto Tarea a crear.

    Returns:
        Tarea: El objeto Tarea creado.
    """
    result = await db["tasks"].insert_one(task.model_dump())
    task_id = result.inserted_id
    return {**task.model_dump(), "_id": str(task_id)}

@router.put("/tasks/{task_id}", response_model=Tarea)
async def update_task(task_id: str, task: Tarea):
    """
    Actualiza una tarea existente.

    Esta función actualiza una tarea en la base de datos utilizando el ID proporcionado.
    Si la tarea no se encuentra, lanza una excepción HTTP 404.

    Args:
        task_id (str): El ID de la tarea a actualizar.
        task (Tarea): El objeto Tarea con los nuevos datos.

    Returns:
        Tarea: El objeto Tarea actualizado.
    ID DE PRUEBA: 67377d455562581293c248e9

    """
    result = await db["tasks"].update_one({"_id": ObjectId(task_id)}, {"$set": task.model_dump()})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """
    Elimina una tarea existente.

    Esta función elimina una tarea de la base de datos utilizando el ID proporcionado.
    Si la tarea no se encuentra, lanza una excepción HTTP 404.

    Args:
        task_id (str): El ID de la tarea a eliminar.

    Returns:
        dict: Un mensaje de éxito si la tarea fue eliminada.
    ID DE PRUEBA: 67377d455562581293c248e9

    """
    result = await db["tasks"].delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"detail": "Tarea eliminada con éxito"}

@router.get("/tasks/habilidad/{habilidad}", response_model=List[Tarea])
async def get_tasks_by_habilidad(habilidad: str):
    """
    Obtiene tareas que requieren una determinada habilidad.

    Esta función busca tareas en la base de datos que requieren la habilidad proporcionada.
    Retorna una lista de objetos de tipo Tarea.

    Args:
        habilidad (str): La habilidad requerida.

    Returns:
        List[Tarea]: Una lista de tareas que requieren la habilidad.
    """
    tasks = await db["tasks"].find({"habilidades": habilidad}).to_list(1000)
    return tasks

@router.get("/tasks/colaborador/{email}", response_model=List[Tarea])
async def get_tasks_by_colaborador(email: str):
    """
    Obtiene tareas asignadas a un determinado colaborador.

    Esta función busca tareas en la base de datos que tienen asignado al colaborador con el email proporcionado.
    Retorna una lista de objetos de tipo Tarea.

    Args:
        email (str): El email del colaborador.

    Returns:
        List[Tarea]: Una lista de tareas asignadas al colaborador.
    """
    tasks = await db["tasks"].find({"colaboradores.email": email}).to_list(1000)
    return tasks


@router.post("/tasks/{task_id}/assign", response_model=Tarea)
async def assign_collaborator(task_id: str, collaborator_email: str):
    """
    Asigna un colaborador a una tarea si tiene las habilidades requeridas.

    Args:
        task_id (str): El ID de la tarea.
        collaborator (dict): Los detalles del colaborador.

    Returns:
        dict: La tarea actualizada con el colaborador asignado.
    ID DE PRUEBA: 67377d455562581293c248e9

    """
    task = await db["tasks"].find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    collaborator = await db["collabs"].find_one({"email": collaborator_email})
    if not collaborator:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")

    if not any(habilidad in task["habilidades"] for habilidad in collaborator["habilidades"]):
        raise HTTPException(status_code=400, detail="El colaborador no posee las habilidades requeridas")

    task["colaboradores"].append({
        "email": collaborator["email"],
        "segmento_asignado": 0  #por defecto
    })

    await db["tasks"].update_one({"_id": ObjectId(task_id)}, {"$set": task})
    return task

@router.get("/tasks/{task_id}/candidates", response_model=List[str])
async def get_candidates_for_task(task_id: str):
    """
    Obtiene una lista de candidatos que tienen las habilidades requeridas para una tarea específica.

    Args:
        task_id (str): El ID de la tarea.

    Returns:
        List[str]: Una lista de emails de candidatos.
    ID DE PRUEBA: 67377d455562581293c248e9
    """
    task = await db["tasks"].find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    candidates = await db["collabs"].find({
        "habilidades": {"$in": task["habilidades"]}
    }).to_list(1000)

    candidate_emails = [candidate["email"] for candidate in candidates]
    return candidate_emails

@router.get("/tasks/completas", response_model=List[Tarea])
async def get_completely_assigned_tasks():
    """
    Obtiene tareas completamente asignadas.

    Esta función busca tareas en la base de datos que tienen asignados tantos colaboradores como segmentos de los que consta la tarea.
    Retorna una lista de objetos de tipo Tarea.

    Returns:
        List[Tarea]: Una lista de tareas completamente asignadas.
    """
    tasks = await db["tasks"].find().to_list(1000)
    completely_assigned_tasks = [task for task in tasks if len(task["colaboradores"]) >= task["segmentos"]]
    return completely_assigned_tasks

