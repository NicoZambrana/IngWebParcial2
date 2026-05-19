# Gestor de tareas

API para la gestión de colaboradores y tareas, desarrollada con FastAPI y MongoDB.

## Tabla de contenidos

- [Descripción](#descripción)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución](#ejecución)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Endpoints Principales](#endpoints-principales)
- [Licencia](#licencia)

---

## Descripción

**ColabManager** es una API que permite:
- Registrar colaboradores con habilidades.
- Asignar colaboradores a tareas, validando que posean las habilidades requeridas.
- Gestionar tareas, habilidades y responsables.
- Consultar candidatos idóneos, tareas completas y responsables.

Incluye arquitectura modular y documentación OpenAPI automática (Swagger UI).

---

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/NicoZambrana/GestorTareas.git
    cd GestorTareas
    ```

2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

---

## Configuración

Crea un archivo `.env` con tus variables de configuración para MongoDB:

```dotenv
MONGODB_URL=mongodb+srv://<usuario>:<password>@<tucluster>.mongodb.net/
DATABASE_NAME=colabmanager
```

---

## Ejecución

Para iniciar el servidor:

```bash
uvicorn app.main:app --reload
```

El API estará disponible en [http://localhost:8000](http://localhost:8000).

La documentación automática (Swagger UI):
- [http://localhost:8000/docs](http://localhost:8000/docs)
- [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Estructura del Proyecto

```
app/
├── routers/
│   ├── collaborator.py
│   ├── skill.py
│   └── task.py
├── config.py
├── database.py
├── main.py
├── models.py
requirements.txt
README.md
.env.example
```

---

## Endpoints principales

- `/collaborators/`  
  CRUD de colaboradores
- `/collaborators/{email}`  
  Detalle, edición y borrado de colaborador
- `/collaborators/{email}/skills`  
  Gestión de habilidades por colaborador
- `/tasks/`  
  CRUD de tareas
- `/tasks/{task_id}/assign`  
  Asignación de colaborador a tarea (verificación de habilidades)
- `/tasks/{task_id}/candidates`  
  Candidatos aptos para una tarea

Más detalles y ejemplos en Swagger UI.

---

## Licencia

MIT

---

**Autor:** Nicolás Zambrana  
Proyecto para Ingeniería Web 2024 Parcial 2
