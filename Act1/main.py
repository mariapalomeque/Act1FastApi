from fastapi import FastAPI, HTTPException

import alumnes
import db_alumnat

from typing import List
from pydantic import BaseModel

app = FastAPI()

class Alumne(BaseModel):
    nomalumne: str
    cicle: str
    curs: int
    grup: str
    idaula: int 

@app.get("/")
def read_root():
    # Retorna un mensaje indicando que la API de alumnos está activa.
    return {"Alumnat API"}

@app.get("/alumne/list", response_model=List[dict])  
def read_alumnes():
    # Obtiene y retorna la lista de todos los alumnos.
    alumne_db = db_alumnat.read_all()
    if not alumne_db:
        raise HTTPException(status_code=404, detail="No se encontraron alumnos")
    alumnes_serialized = alumnes.alumnes_schema(alumne_db)
    return alumnes_serialized

@app.get("/alumne/show/{id}", response_model=dict)
def read_alumne(id: int):
    # Busca y retorna un alumno específico según su ID.
    alumne_db = db_alumnat.read_id(id)  
    if not alumne_db:
        raise HTTPException(status_code=404, detail="No se encontró el alumno")  
    alumne_serialized = alumnes.alumne_schema(alumne_db)
    return alumne_serialized

@app.post("/alumne/add", response_model=dict)
def add_alumne(alumne: Alumne):
    # Agrega un nuevo alumno a la base de datos.
    aula_exists = db_alumnat.check_aula_exists(alumne.idaula) 
    if not aula_exists:
        raise HTTPException(status_code=400, detail="Id de aula no correcta")
    db_alumnat.add_alumne(alumne.nomalumne, alumne.cicle, alumne.curs, alumne.grup, alumne.idaula) 

    return {"message": "S'ha afegit correctament"}

@app.delete("/alumne/delete/{id}", response_model=dict)
def delete_alumne(id: int):
    # Elimina un alumno de la base de datos según su ID.
    deleted_filas = db_alumnat.delete_alumne(id)
    if deleted_filas == 0:
        raise HTTPException(status_code=404, detail="No se encontró el alumno")  
    
    return {"message": "S'ha esborrat correctament"}

@app.put("/alumne/update/{id}", response_model=dict)
def update_alumne(id: int, alumne: Alumne):
    # Actualiza los datos de un alumno en la base de datos.
    if alumne.idaula is not None:
        aula_exists = db_alumnat.check_aula_exists(alumne.idaula)
        if not aula_exists:
            raise HTTPException(status_code=400, detail="Id de aula no correcta")

    updated_filas = db_alumnat.update_alumne(id, alumne.nomalumne, alumne.cicle, alumne.curs, alumne.grup, alumne.idaula)
    
    if updated_filas == 0:
        raise HTTPException(status_code=404, detail="No se encontró el alumno") 
    return {"message": "S’ha modificat correctament"}
