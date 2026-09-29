from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import psycopg2

app = FastAPI(title="Clasificador de Commits - Eco Motor IA", version="1.0")

class CommitRequest(BaseModel):
    commit_hash: str
    mensaje: str

def obtener_conexion():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "postgres"),
        user=os.getenv("POSTGRES_USER", "app_ia"),
        password=os.getenv("POSTGRES_PASSWORD", "secreto_seguro"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )

@app.get("/health")
def health_check():
    return {"estado": "ok", "motor": "eco-motor-local activo"}

@app.post("/clasificar")
def clasificar_commit(data: CommitRequest):
    # Eco motor / Clasificación basada en palabras clave
    mensaje_lower = data.mensaje.lower()
    if "fix" in mensaje_lower or "bug" in mensaje_lower:
        categoria = "Corrección de errores (Bugfix)"
    elif "feat" in mensaje_lower or "add" in mensaje_lower:
        categoria = "Nueva característica (Feature)"
    else:
        categoria = "Actualización general / Refactor"

    # Guardar en la base de datos db-ia
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO inferencias (commit_hash, resultado_clasificacion, motor_usado) VALUES (%s, %s, %s)",
            (data.commit_hash, categoria, "eco-motor-local")
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando en BD: {str(e)}")

    return {
        "commit_hash": data.commit_hash,
        "clasificacion": categoria,
        "motor": "eco-motor-local",
        "estado": "Guardado exitosamente en db-ia"
    }

@app.get("/inferencias")
def listar_inferencias():
    try:
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("SELECT id, commit_hash, resultado_clasificacion, motor_usado, creado_en FROM inferencias ORDER BY id DESC;")
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        
        resultado = []
        for fila in filas:
            resultado.append({
                "id": fila[0],
                "commit_hash": fila[1],
                "clasificacion": fila[2],
                "motor": fila[3],
                "creado_en": str(fila[4])
            })
        return {"inferencias": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando la BD: {str(e)}")