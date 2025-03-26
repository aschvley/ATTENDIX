import numpy as np
import json
from database.db import get_connection
from config import RECOGNITION_THRESHOLD

def get_known_embeddings():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, cedula, embedding FROM estudiantes")

    conocidos = []
    for row in cursor.fetchall():
        emb_array = np.array(json.loads(row["embedding"]))  # Convertir JSON a lista y luego a array de NumPy
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
        embedding_array = np.array(estudiante["embedding"])
        distancia = np.linalg.norm(embedding - embedding_array)
        if distancia < RECOGNITION_THRESHOLD:
            return estudiante  # Retornamos el dict completo del estudiante
    return None