from client import db_client
from fastapi import HTTPException

def read_all():
    # Obtiene todos los alumnos de la base de datos.
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM alumne")
        alumne = cur.fetchall()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de conexión: {e}"}
    
    finally:
        conn.close()
    
    return alumne


def read_id(id):
    # Busca y retorna un alumno específico según su ID.
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM alumne WHERE IdAlumne = %s", (id,))  # Corregido
        alumne = cur.fetchone()
            
    except Exception as e:
        return {"status": -1, "message": f"Error de conexión: {e}"}
    
    finally:
        conn.close()
    
    return alumne

def check_aula_exists(idaula):
    # Verifica si la ID del aula existe en la tabla de aulas.
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM aula WHERE IdAula = %s", (idaula,))
        aula = cur.fetchone()
        return aula is not None  
    except Exception as e:
        return False  
    finally:
        conn.close()

def add_alumne(nomalumne, cicle, curs, grup, idaula):
    # Agrega un nuevo alumno a la base de datos.
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "INSERT INTO alumne (NomAlumne, Cicle, Curs, Grup, IdAula, CreatedAt, UpdatedAt) VALUES (%s, %s, %s, %s, %s, NOW(), NOW())"
        cur.execute(query, (nomalumne, cicle, curs, grup, idaula))
        conn.commit()  
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Error al añadir el alumno: {e}")
    finally:
        conn.close()

def delete_alumne(id):
    # Elimina un alumno de la base de datos según su ID.
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "DELETE FROM alumne WHERE IdAlumne = %s"
        cur.execute(query, (id,))
        conn.commit()  
        return cur.rowcount  
    except Exception as e:
        return HTTPException(status_code=400, detail=f"Error al eliminar el alumno: {e}")
    finally:
        conn.close()

def update_alumne(id, nomalumne, cicle, curs, grup, idaula):
    # Actualiza los datos de un alumno en la base de datos.
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "UPDATE alumne SET NomAlumne = %s, Cicle = %s, Curs = %s, Grup = %s, IdAula = %s WHERE IdAlumne = %s"
        cur.execute(query, (nomalumne, cicle, curs, grup, idaula, id))
        conn.commit()  
        return cur.rowcount 
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al editar el alumno: {e}")
    finally:
        conn.close()
