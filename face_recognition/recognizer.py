import numpy as np
from database.db import get_connection
from config import RECOGNITION_THRESHOLD
from ast import literal_eval  # para convertir string a lista segura

def get_known_embeddings():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, cedula, embedding FROM estudiantes")

    conocidos = []
    for row in cursor.fetchall():
        emb_array = np.array(literal_eval(row["embedding"]))  # Convertimos el string a array
        conocidos.append({
            "id": row["id"],
            "nombre": row["nombre"],
            "cedula": row["cedula"],
            "embedding": emb_array
        })

    conn.close()
    return conocidos

def recognize_face(embedding):
    estudiantes = get_known_embeddings()
    for estudiante in estudiantes:
        distancia = np.linalg.norm(embedding - estudiante["embedding"])
        if distancia < RECOGNITION_THRESHOLD:
            return estudiante  # Retornamos el dict completo del estudiante
    return None
