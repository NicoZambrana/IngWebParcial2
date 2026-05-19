from fastapi import FastAPI
from .routers import collaborator, skill, task

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Has entrado a la pagina web Gente!"}




app.include_router(task.router)
app.include_router(collaborator.router)
app.include_router(skill.router)